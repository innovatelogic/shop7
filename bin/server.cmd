@echo off

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/server/receive.py""

python %SCRIPT% %*
::python %BUILD_DB%

ECHO ERRORLEVEL=%ERRORLEVEL%