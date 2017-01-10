#!/bin/bash -ex
source venv/bin/activate
python2.7 -m py_compile ./deploy.py
python2.7 -m py_compile ./labcafe.py

aws cloudformation validate-template --template-body "$(cat aws-lab-cafe.cfn)"

cd putty-0.67
chmod ugo+x ./configure
./configure --without-gtk
make -j 4
cd ..
cp putty-0.67/puttygen bin/puttygen

virtualenv --relocatable venv
