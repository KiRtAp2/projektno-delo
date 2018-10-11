#!/bin/sh
export YOURAPPLICATION_SETTINGS=../config.cfg
python3 koda/main.py --db-create-all
