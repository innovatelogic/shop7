@echo off

call %~dp0/config/server_config.cmd

set INPUT=%~dp0../data/categories.xlsx
set OUT=%~dp0../data/cache
set ASPECT=prom_ua

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/xlsx_groups_exporter/launcher.py --input %INPUT% --out %OUT% --aspect %ASPECT%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%