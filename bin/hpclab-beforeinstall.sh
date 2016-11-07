#!/bin/bash
virtualenv /webapps/hpc-lab-maker
echo "pwd before pip: $(pwd)"
pip install --requirement requirements.txt --upgrade
