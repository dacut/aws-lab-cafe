#!/usr/bin/env python2.7
from __future__ import absolute_import, print_function
from json import dump as json_dump, dumps as json_dumps
from os import chdir, environ, makedirs
import requests
from shutil import copytree
from traceback import print_exc
from urlparse import urlparse
from zappa.cli import ZappaCLI

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

    copytree(environ["LAMBDA_RUNTIME_DIR"], "/tmp/zappa")
    chdir("/tmp/zappa")
    update_zappa_settings(event)

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
    except Exception as e:
        print_exc()
        status = "FAILED"
        reason = str(e)

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
    r = requests.put(response_url, headers=headers, data=body)
    print("Result: %d %s" % (r.status_code, r.reason))
    return