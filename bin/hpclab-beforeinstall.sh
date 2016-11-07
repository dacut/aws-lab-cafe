#!/bin/bash
DEPLOYMENT_ARCHIVE=/opt/codedeploy-agent/deployment-root/${DEPLOYMENT_GROUP_ID}/${DEPLOYMENT_ID}/deployment-archive
virtualenv /webapps/hpc-lab-maker
echo "Deployment archive: $DEPLOYMENT_ARCHIVE"
pip install --requirement $DEPLOYMENT_ARCHIVE/requirements.txt --upgrade
