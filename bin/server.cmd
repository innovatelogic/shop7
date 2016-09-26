@echo off

call %~dp0/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/server/launch.py --host %MASTER_SERVER_HOST% --db_name %MASTER_DB_NAME%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%