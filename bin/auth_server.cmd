@echo off

call %~dp0/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0..\src\server\auth\launch.py --host %AUTH_SERVER_HOST% --port %AUTH_SERVER_PORT%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%