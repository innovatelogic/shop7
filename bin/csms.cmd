@echo off

call %~dp0/config/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/cmsc/launcher.py""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%