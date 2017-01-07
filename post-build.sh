#!/bin/bash -ex
rm -f aws-lab-cafe.zip
zip -q aws-lab-cafe.zip ./labcafe.pyc ./labcafe.py ./zappa_settings.json
pwd
cd venv/lib/python2.7/site-packages
ls -l
zip -q -u -r ../../../../aws-lab-cafe.zip .
cd $CODEBUILD_SRC_DIR
aws s3 cp aws-lab-cafe.zip s3://cuthbert-labcafe-artifacts
