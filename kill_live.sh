#!/bin/bash

pid_str=$(ps -aux | grep "python3 run_live_demo.py" | grep -v grep)

echo $pid_str

pid=$(echo $pid_str | awk '{print $2}')
echo $pid

kill $pid
