@echo off

call %~dp0/server_config.cmd

set INPUT=%~dp0../data/base_aspect.xml
set OUT=%~dp0../data/cache

set NITEM=100

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/base_aspect_import/launcher.py""
set PARAMS=""--input %INPUT% --out %OUT%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %PARAMS% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%