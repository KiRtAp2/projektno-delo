#!/bin/sh
export OAUTHLIB_INSECURE_TRANSPORT=1
export YOURAPPLICATION_SETTINGS=../config.cfg
python3 koda/main.py --db-create-all
python3 modify_base.py --file baza/seznam.txt

