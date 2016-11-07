#!/bin/bash -e
VIRTUAL_ENV=/webapps/hpc-lab-maker
PATH=$VIRTUAL_ENV/bin:$PATH
export PATH VIRTUAL_ENV
! test -e $VIRTUAL_ENV/run || rm -rf $VIRTUAL_ENV/run
! test -e $VIRTUAL_ENV/log || rm -rf $VIRTUAL_ENV/log
cd $VIRTUAL_ENV
FLASK_APP=hpclab.py $VIRTUAL_ENV/bin/flask run \
  > $VIRTUAL_ENV/log/hpc-lab-maker.log 2>&1 &
echo $! > $VIRTUAL_ENV/run/flask.pid
disown %1
