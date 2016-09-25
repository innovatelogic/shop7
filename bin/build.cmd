@echo off

set DATA_FOLDER="%~dp0../data/"
set OUT="%~dp0../data"

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/utils/xlsx_exporter/build.py --all --input %DATA_FOLDER% --out %OUT%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%