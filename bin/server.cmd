@echo off

call %~dp0/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/server/launch.py --host %MASTER_SERVER_HOST% --ms_auth_queue %MS_AUTH_QUEUE_NAME%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%