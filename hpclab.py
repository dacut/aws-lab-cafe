#!/usr/bin/env python2.7
from cStringIO import StringIO
from base64 import b64encode
from boto3.session import Session as Boto3Session
from flask import Flask, g, render_template, request
from flask_login import LoginManager

app = Flask(__name__)

API_ENDPOINT = "https://0hud6wdi6a.execute-api.us-west-2.amazonaws.com/dev"

@app.route("/", methods=["GET"], defaults={'page': "index.html"})
@app.route("/<path:page>", methods=["GET"])
def index(page, **kw):
    return render_template(page)
