#!/bin/bash -ex
SITE_PACKAGES=venv/lib/python2.7/site-packages

# Copy cracklib libraries to the site-packages directory
cp -p /usr/lib64/libcrack* $SITE_PACKAGES

# Remove OpenCV from lambda-packages (too big) and Lambda-included packages
if [[ -d $SITE_PACKAGES/lambda_packages/OpenCV ]]; then
    rm -r $SITE_PACKAGES/lambda_packages/OpenCV
fi;

# Remove botocore, boto3, and jmespath; they're included
rm -rf $SITE_PACKAGES/botocore* $SITE_PACKAGES/boto3* $SITE_PACKAGES/jmespath*

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
  ./templates \
  ./venv

# Upload the Lambda bundle to S3.
aws s3 cp aws-lab-cafe.zip s3://cuthbert-labcafe-artifacts --quiet

# Upload the CloudFormation template to S3.
aws s3 cp aws-lab-cafe.cfn s3://cuthbert-labcafe-artifacts --quiet

# Upload the test parameters to S3.
aws s3 cp aws-lab-cafe-test.json s3://cuthbert-labcafe-artifacts --quiet
