@echo off

call %~dp0/server_config.cmd

set DATA_FOLDER="%~dp0../data/"
set OUT="%~dp0../data"

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/xlsx_exporter/build.py --all --input %DATA_FOLDER% --out %OUT%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%