#!/usr/bin/env python2.7
from __future__ import absolute_import, print_function
from json import dump as json_dump, dumps as json_dumps
from os import chdir, environ, listdir, makedirs, readlink
from os.path import isfile, isdir, islink
from shutil import copytree, rmtree
import sys
from time import gmtime, strftime
from traceback import format_exc, print_exc
from urlparse import urlparse

def update_zappa_settings(event):
    resource_props = event.get("ResourceProperties")
    if resource_props is None:
        raise RuntimeError("ResourceProperties not available from CloudFormation")

    enc_key_id = resource_props.get("EncryptionKeyId")
    if enc_key_id is None:
        raise RuntimeError("EncryptionKeyId not specified")

    stack_name = resource_props.get("StackName")
    if stack_name is None:
        raise RuntimeError("StackName not specified")

    region = resource_props.get("Region")
    if region is None:
        raise RuntimeError("Region not specified")

    s3_bucket = resource_props.get("S3Bucket")
    if s3_bucket is None:
        raise RuntimeError("S3Bucket not specified")

    logical_resource_id = event["LogicalResourceId"]
    if "PhysicalResourceId" not in event:
        event["PhysicalResourceId"] = (
            "%s-%s-Zappa" % (stack_name, logical_resource_id))

    debug = resource_props.get("Debug", "FALSE")
    domain_name = resource_props.get("DomainName")

    env_config = {
        "app_function": "labcafe.app",
        "aws_region": region,
        "delete_local_zip": False,
        "delete_s3_zip": True,
        "environment_variables": {
            "DEBUG": debug,
            "ENCRYPTION_KEY_ID": enc_key_id,
            "LABCAFE_TABLE_PREFIX": stack_name + ".",
        },
        "lambda_description": ("%s renderer" % (stack_name,)),
        "project_name": ("%s-Zappa" % (stack_name,)),
        "s3_bucket": s3_bucket,
        "timeout_seconds": 5,
        "use_precompiled_packages": False,
    }
    if domain_name:
        env_config["domain"] = domain_name

    zsettings = { logical_resource_id: env_config }
    with open("zappa_settings.json", "w") as fd:
        json_dump(zsettings, fd)

    return

def handle_zappa(event, context):
    request_type = event["RequestType"]
    logical_resource_id = event["LogicalResourceId"]

    if exists("/tmp/zappa"):
        rmtree("/tmp/zappa")
    copytree(environ["LAMBDA_TASK_ROOT"], "/tmp/zappa", symlinks=True)
    chdir("/tmp/zappa")
    sys.path[:0] = [
        "/tmp/zappa",
        "/tmp/zappa/venv/lib/python2.7",
        "/tmp/zappa/venv/lib/python2.7/site-packages"]
    environ["PATH"] = "/tmp/zappa/venv/bin:" + environ["PATH"]
    environ["VIRTUAL_ENV"] = "/tmp/zappa/venv"

    update_zappa_settings(event)

    from zappa.cli import ZappaCLI
    zcli = ZappaCLI()
    if request_type in "Create":
        if zcli.handle(["deploy", logical_resource_id]):
            raise RuntimeError("Zappa deployment failed")
    elif request_type == "Update":
        if zcli.handle(["update", logical_resource_id]):
            raise RuntimeError("Zappa update failed")
    elif request_type == "Delete":
        if zcli.handle(["undeploy", logical_resource_id]):
            raise RuntimeError("Zappa undeploy failed")

    return

def handler(event, context):
    """
    Manage AWS Lab Cafe deployment using Zappa.
    """
    print(str(event))
    sys.path.append(environ["LAMBDA_TASK_ROOT"] + "/venv/lib/python2.7")
    sys.path.append(environ["LAMBDA_TASK_ROOT"] + "/venv/lib/python2.7/site-packages")
    resource_type = event["ResourceType"]

    try:
        if resource_type == "Custom::Zappa":
            result = handle_zappa(event, context)
        else:
            raise RuntimeError("Unknown resource type %s" % resource_type)

        if result is None:
            result = {}
        elif not isinstance(result, dict):
            raise TypeError("Expected a dict or None from handler, got %s" %
                            type(result).__name__)

        status = "SUCCESS"
    except ImportError:
        from cStringIO import StringIO
        result = StringIO()

        result.write(format_exc())
        result.write("\n")

        result.write("sys.path=%r\n" % sys.path)

        for pathel in sys.path:
            result.write("%s/\n" % pathel)

            try:
                for filename in listdir(pathel):
                    result.write("    %s" % filename)

                    pathname = pathel + "/" + filename
                    if isdir(pathname):
                        result.write("/")
                    elif islink(pathname):
                        result.write("@ -> %s" % readlink(pathname))

                    result.write("\n")
            except OSError as e:
                result.write("    %s\n" % e)

        key = "deploy-debug-" + strftime("%Y%m%dT%H%M%SZ", gmtime()) + ".txt"
        import boto3.session
        b3 = boto3.session.Session(region_name="us-west-2")
        s3 = b3.client("s3")
        s3.put_object(ACL="private", Bucket="cuthbert-labcafe-artifacts",
                      Key=key, Body=result.getvalue())
        print("Debugging output written to s3://cuthbert-labcafe-artifacts/%s" % key)

        raise
    except Exception as e:
        print_exc()
        status = "FAILED"
        reason = str(e)
        result = {}

    response_url = event["ResponseURL"]
    reponse_host = urlparse(response_url).netloc
    stack_id = event["StackId"]
    request_id = event["RequestId"]
    logical_resource_id = event["LogicalResourceId"]
    physical_resource_id = event.get(
        "PhysicalResourceId",
        result.pop("PhysicalResourceId", logical_resource_id))

    body = {
        "Status": status,
        "StackId": stack_id,
        "RequestId": request_id,
        "LogicalResourceId": logical_resource_id,
        "PhysicalResourceId": physical_resource_id,
        "Data": result,
    }
    body = json_dumps(body)

    headers = {
        "Content-Type": "",
        "Content-Length": len(body)
    }

    print("Sending response to %s" % response_url)
    print(body)
    import requests
    r = requests.put(response_url, headers=headers, data=body)
    print("Result: %d %s" % (r.status_code, r.reason))
    return
