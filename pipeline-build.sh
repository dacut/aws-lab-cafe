#!/bin/bash -ex
python2.7 -m py_compile labcafe.py

mkdir artifacts
cp -a static templates labcafe.py defaults.cfg requirements.txt artifacts

cd putty-0.67
chmod ugo+x ./configure
./configure
make -j 4
cd ..
cp putty-0.67/puttygen artifacts/bin/puttygen
