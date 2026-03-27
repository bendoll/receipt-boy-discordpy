@echo off
title receipt-boy-discordpy
color 2
:start
python ./main.py
echo python crashed, restarting...
goto start