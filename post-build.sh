#!/bin/bash -ex
# Always start with a fresh Lambda bundle.
rm -f aws-lab-cafe.zip

# Add our app.
zip -q aws-lab-cafe.zip ./labcafe.pyc ./labcafe.py ./zappa_settings.json


# Add site-packages to the root of the Lambda bundle.
cd venv/lib/python2.7/site-packages

# Copy cracklib libraries to the site-packages directory
cp -p /usr/lib64/libcrack* .
zip -q -u -r ../../../../aws-lab-cafe.zip .

# Upload the Lambda bundle to S3.
cd $CODEBUILD_SRC_DIR
aws s3 cp aws-lab-cafe.zip s3://cuthbert-labcafe-artifacts
