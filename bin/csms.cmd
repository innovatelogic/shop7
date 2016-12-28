@echo off

call %~dp0/config/server_config.cmd
set INPUT=%~dp0../data/

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/cmsc/launcher.py""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""
set PARAMS=""--input %INPUT%""

python %SCRIPT% %PARAMS% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%