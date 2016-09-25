@echo off

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/server/receive.py""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%