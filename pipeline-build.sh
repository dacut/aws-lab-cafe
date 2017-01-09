#!/bin/bash -ex
source venv/bin/activate
python2.7 -m py_compile ./labcafe.py
python2.7 ./generate-zappa-settings.py

cd putty-0.67
chmod ugo+x ./configure
./configure --without-gtk
make -j 4
cd ..
cp putty-0.67/puttygen bin/puttygen
