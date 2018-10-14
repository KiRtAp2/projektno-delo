#!/bin/sh
export OAUTHLIB_INSECURE_TRANSPORT=1
export YOURAPPLICATION_SETTINGS=../config.cfg
python3 koda/main.py
