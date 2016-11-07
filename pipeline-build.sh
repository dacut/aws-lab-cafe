#!/bin/bash -e
test -d venv && rm -r venv
virtualenv venv/pipeline
source venv/pipeline/bin/activate
pip install -r requirements.txt
cp bin/hpclab-start.sh bin/hpclab-stop.sh venv/pipeline/bin
cp appspec.yml venv/pipeline
cp -a hpclab.py static templates venv/pipeline
deactivate
