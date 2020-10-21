#!/usr/bin/env bash

if [ -z "$1" ];then
    echo "Puoi utilizzare"
    echo "1) test 2) install"
    echo "per selezionare le cartelle"
    exit 0
fi

PYTHONPATH=$(pwd) python3 $1/$2