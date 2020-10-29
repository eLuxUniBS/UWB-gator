#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Puoi utilizzare"
  echo "1) test 2) install 3) ."
  echo "per selezionare le cartelle"
  exit 0
fi

if [ -z "$2" ]; then
  PYTHONPATH=$(pwd) python3 main_subs.py &
  PYTHONPATH=$(pwd) python3 main_pubs.py
  exit 0
fi

PYTHONPATH=$(pwd) python3 $1/$2
