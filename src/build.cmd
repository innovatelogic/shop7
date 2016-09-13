@echo off

set PYTHON="%python%"
set SCRIPT=""-u %~dp0build.py --goal tools_build --out %OUT%""
set BUILD_DB="%~dp0build_db.py"

::python %SCRIPT% %*
python %BUILD_DB%

ECHO ERRORLEVEL=%ERRORLEVEL%