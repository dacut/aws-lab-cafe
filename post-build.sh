#!/bin/bash -ex

# Add our app.
zip -q -r aws-lab-cafe.zip \
  ./deploy.py \
  ./deploy.pyc \
  ./labcafe.py \
  ./labcafe.pyc \
  ./secretgen.py \
  ./secretgen.pyc \
  ./bin \
  ./static \
  ./templates

# Add site-packages to the root of the Lambda bundle.
cd venv/lib/python2.7/site-packages

# Copy cracklib libraries to the site-packages directory
cp -p /usr/lib64/libcrack* .

# Remove OpenCV from lambda-packages (too big)
rm -r lambda_packages/OpenCV

# Remove botocore, boto3, and jmespath; they're included
rm -rf botocore* boto3* jmespath*

# Add site-packages to the bundle
zip -q -u -r ../../../../aws-lab-cafe.zip .

# Upload the Lambda bundle to S3.
cd $CODEBUILD_SRC_DIR
aws s3 cp aws-lab-cafe.zip s3://cuthbert-labcafe-artifacts

# Upload the CloudFormation template to S3.
aws s3 cp aws-lab-cafe.cfn s3://cuthbert-labcafe-artifacts

# Upload the test parameters to S3.
aws s3 cp aws-lab-cafe-test.json s3://cuthbert-labcafe-artifacts
