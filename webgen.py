#!/usr/bin/env python2.7
from __future__ import absolute_import, print_function
from boto3.session import Session
from jinja2 import Environment, PackageLoader

bucket = "portable-hpc-lab"
templates = ["index.html", "error.html"]
template_context = {
    "static_prefix": "/static/",
    "api_endpoint": "https://0hud6wdi6a.execute-api.us-west-2.amazonaws.com/dev",
}

env = Environment(loader=PackageLoader("webgen", "templates"))
s3 = Session(profile_name="scilab", region_name="us-west-2").client("s3")

for filename in templates:
    template = env.get_template(filename)
    data = template.render(**template_context)
    s3.put_object(
        Body=data, Bucket=bucket, ContentEncoding="utf-8",
        ContentType="text/html", Key=filename)
