#!/bin/bash


SCRIPT="scripts/experience_collect.py"


END_ID=23

# episode id loop from XX to runtime
for i in $(seq 23 $END_ID)
do
    echo "Running episode $i..."

    # /home/cloud/program/miniconda3/envs/controller/bin/python $SCRIPT $i
    /home/cloud/.miniconda3/envs/controller/bin/python $SCRIPT $i
    sleep 15
    echo "Finished episode $i."
done

echo "All episodes completed."