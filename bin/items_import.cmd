@echo off

call %~dp0/config/server_config.cmd

set INPUT=%~dp0../data/data.xlsx
set OUT=%~dp0../data/cache
set NITEM=100
set ASPECT=prom_ua

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/xlsx_exporter/launcher.py""
set PARAMS=""--all --input %INPUT% --out %OUT% --mapping cat_mapping.map --user admin --nitem %NITEM% --aspect %ASPECT%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %PARAMS% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%