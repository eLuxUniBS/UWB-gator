#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Errore, devi indicare il seriale di riferimento"
  exit 2
fi

SERIAL="$1"
CURRENTDATE=`date +"%Y-%m-%dT%T"`
mkdir -p ./logs
FILE_DATA="./logs/log_$CURRENTDATE.logs"
echo "$CURRENTDATE read $SERIAL and put it into $FILE_DATA"
minicom -D $SERIAL -S ./monitoring_data > $FILE_DATA