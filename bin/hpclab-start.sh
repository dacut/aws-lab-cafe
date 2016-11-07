#!/bin/bash -e
source /webapps/hpc-lab-maker/bin/activate

test -d $VIRTUAL_ENV/run || mkdir -p $VIRTUAL_ENV/run
test -d $VIRTUAL_ENV/log || mkdir -p $VIRTUAL_ENV/log
cd $VIRTUAL_ENV
FLASK_APP=hpclab.py $VIRTUAL_ENV/bin/flask run --host=0.0.0.0 \
  > $VIRTUAL_ENV/log/hpc-lab-maker.log 2>&1 &
echo $! > $VIRTUAL_ENV/run/flask.pid
disown %1
