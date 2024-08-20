#!/bin/bash


SCRIPT="scripts/experience_collect.py"


RUN_TIMES=20

# 循环运行指定次数
for i in $(seq 13 $RUN_TIMES)
do
    echo "Running episode $i..."

    /home/cloud/program/miniconda3/envs/controller/bin/python $SCRIPT $i
    sleep 15
    echo "Finished episode $i."
done

echo "All episodes completed."