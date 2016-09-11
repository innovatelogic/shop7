@echo off

set PYTHON="%python%"
set SCRIPT=""-u %~dp0build.py --goal tools_build --out %OUT%""

python %SCRIPT% %*

ECHO ERRORLEVEL=%ERRORLEVEL%