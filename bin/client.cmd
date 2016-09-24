@echo off

call %~dp0/local_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/client/launch.py --auth_host %AUTH_SERVER_HOST% --auth_port %AUTH_SERVER_PORT%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%