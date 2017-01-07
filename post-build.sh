#!/bin/bash -ex
TZ=UTC; export TZ
DATETIME=$(date +'%Y%m%dT%H%M%SZ')
# Add our app.
zip -q aws-lab-cafe-${DATETIME}.zip ./labcafe.pyc ./labcafe.py ./zappa_settings.json


# Add site-packages to the root of the Lambda bundle.
cd venv/lib/python2.7/site-packages

# Copy cracklib libraries to the site-packages directory
cp -p /usr/lib64/libcrack* .
zip -q -u -r ../../../../aws-lab-cafe-${DATETIME}.zip .

# Upload the Lambda bundle to S3.
cd $CODEBUILD_SRC_DIR
aws s3 cp aws-lab-cafe-${DATETIME}.zip s3://cuthbert-labcafe-artifacts

# Modify the CloudFormation script
mv aws-lab-cafe.cfn aws-lab-cafe.cfn.in
sed -e "s/@@DATETIME@@/${DATETIME}/g" aws-lab-cafe.cfn.in > aws-lab-cafe.cfn
