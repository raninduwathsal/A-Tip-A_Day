#!/bin/bash
sleep $(( (RANDOM * 1000 + RANDOM) % 46800 ))
/usr/bin/python3 /home/debian/A-Tip-A_Day/daily_tip_logger.py >> /home/debian/daily_tip.log 2>&1

