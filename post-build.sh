#!/bin/bash -ex
rm -f aws-lab-cafe.zip
zip aws-lab-cafe.zip ./labcafe.pyc ./labcafe.py ./zappa_settings.json
ls -l
ls -l venv/lib/python2.7/site-packages
pwd
cd venv/lib/python2.7/site-packages
pwd
cd venv/lib/python2.7/site-packages && zip -u -r ../../../../aws-lab-cafe.zip .
aws s3 cp aws-lab-cafe.zip s3://cuthbert-labcafe-artifacts
