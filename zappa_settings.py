from __future__ import absolute_import, print_function
from distutils.util import strtobool
from os import environ

API_STAGE = "prod"
APP_MODULE = "labcafe"
APP_FUNCTION = "app"
AWS_EVENT_MAPPING = {}
DEBUG = strtobool(environ.get("DEBUG", "false"))
DJANGO_SETTINGS = None
DOMAIN = environ.get("DOMAIN")
ENVIRONMENT_VARIABLES = {}
EXCEPTION_HANDLER = None
EXECUTION_HANDLER = None
LOG_LEVEL = ("DEBUG" if DEBUG else "INFO")
PROJECT_NAME = "LabCafe"
