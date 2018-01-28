@echo off

call %~dp0/config/local_config.cmd

set DEF_LOGIN=admin	
set DEF_PASS=admin

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/client/launch.py --auth_host %AUTH_SERVER_HOST% --auth_port %AUTH_SERVER_PORT% --login %DEF_LOGIN% --password=%DEF_PASS%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%