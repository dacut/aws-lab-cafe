#!/usr/bin/env python2.7
from cStringIO import StringIO
from base64 import b64encode
from boto3.session import Session as Boto3Session
from flask import Flask, g, render_template, request
from flask_login import LoginManager

app = Flask(__name__)

API_ENDPOINT = "https://0hud6wdi6a.execute-api.us-west-2.amazonaws.com/dev"

@app.route("/{path+}", methods=["GET", "POST", "PUT"])
def index(*args, **kw):
    result = StringIO()
    result.write("request:\n")
    result.write(str(request) + "\n")
    result.write("args:\n")
    for i, arg in enumerate(args):
        result.write("%2d %s\n" % (i, arg))

    result.write("\n\nkw:\n")
    for key, value in kw.iteritems():
        result.write("%s=%r\n" % (key, value))

    return result.getvalue()
