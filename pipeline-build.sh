#!/bin/bash -e
test -d venv && rm -r venv
virtualenv venv/pipeline
source venv/pipeline/bin/activate
pip -r requirements.txt
python ./setup.py build
python ./setup.py install
