#!/bin/bash -e
test -d venv && rm -r venv
virtualenv venv/pipeline
source venv/pipeline/bin/activate
python ./setup.py build
python ./setup.py install
cp bin/hpclab-start.sh bin/hpclab-stop.sh venv/pipeline/bin
cp appspec.yml venv/pipeline
deactivate
