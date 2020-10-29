#!/usr/bin/env bash

if [ -z "$1" ]; then
  PYTHONPATH=$(pwd) python3 main_subs.py &
  PYTHONPATH=$(pwd) python3 main_pubs.py
else


PYTHONPATH=$(pwd) python3 main_$1.py
fi