#!/bin/bash


SCRIPT="scripts/experience_collect.py"


RUN_TIMES=10

# 循环运行指定次数
for i in $(seq 1 $RUN_TIMES)
do
    echo "Running episode $i..."

    /home/cloud/program/miniconda3/envs/controller/bin/python $SCRIPT $i
    
    echo "Finished episode $i."
done

echo "All episodes completed."