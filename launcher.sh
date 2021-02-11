#!/usr/bin/env bash

if [ -z "$2" ];then
  if [ -z "$1" ]; then
    PYTHONPATH=$(pwd) python3 main_geo.py &
    PYTHONPATH=$(pwd) python3 main_net.py
  else
    PYTHONPATH=$(pwd) python3 main_$1.py
  fi
  else
    PYTHONPATH=$(pwd) python3 main_$1.py $2 $3
fi