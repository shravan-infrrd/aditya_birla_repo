#!/usr/bin/env bash
source /home/ubuntu/aditya_birla/venv/bin/activate
nohup gunicorn -b 0.0.0.0:6790 -t 500 -w 3 endpoint:app &
