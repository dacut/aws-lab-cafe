from __future__ import absolute_import, print_function
from distutils.util import strtobool
from os import environ

APP_MODULE = "labcafe"
APP_FUNCTION = "app"
EXECUTION_HANDLER = None
DEBUG = strtobool(environ.get("DEBUG", "false"))
LOG_LEVEL = ("DEBUG" if DEBUG else "INFO")
DOMAIN = environ.get("DOMAIN")
API_STAGE = "prod"
PROJECT_NAME = "LabCafe"
