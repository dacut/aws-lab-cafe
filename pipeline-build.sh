#!/bin/bash -ex
mkdir pipeline
cp -a bin static templates appspec.yml hpclab.py hpclab*.cfg requirements.txt pipeline

cd putty-0.67
autoconf
./configure
make -j 4
cd ..
cp putty-0.67/puttygen pipeline/bin/puttygen
