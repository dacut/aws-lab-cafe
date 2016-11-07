#!/bin/bash -e
source /webapps/hpc-lab-maker/bin/activate

if [[ -r $VIRTUAL_ENV/run/flask.pid ]]; then
    flask_pid=$(cat $VIRTUAL_ENV/run/flask.pid)

    echo "Killing Flask executable PID $flask_pid";
    kill $flask_pid;

    sleep_time=0;
    while kill -0 $flask_pid && [[ $sleep_time -lt 10 ]]; do
        sleep 1;
        sleep_time=$(($sleep_time + 1));
    done;

    if ! kill -0 $flask_pid; then
        echo "Forcibly killing Flask executable $flask_pid";
        kill -9 $flask_pid || true
    fi;

    rm $VIRTUAL_ENV/run/flask.pid;
fi;
