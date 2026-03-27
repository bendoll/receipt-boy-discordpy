@echo off
title installng deps for receipt-boy-discordpy
color 2
echo Installing dependencies...
pip install discord.py python-dotenv requests pillow python-escpos
set /p startnow=start the bot now? (Y/[N])
if /i "%startnow%" neq "y" goto end
CALL ./start-win.bat
:end
echo done!
pause