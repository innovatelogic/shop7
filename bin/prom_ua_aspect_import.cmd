@echo off

call %~dp0/config/server_config.cmd

set INPUT=%~dp0../data/prom_ua.xml
set OUT=%~dp0../data/cache
set ASPECT=prom_ua

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/base_aspect_import/launcher.py""
set PARAMS=""--input %INPUT% --out %OUT% --aspect %ASPECT%""

set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %PARAMS% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%