@echo off

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/build.py --all --out %OUT%""
set BUILD_DB="%~dp0build_db.py"

python %SCRIPT% %*
::python %BUILD_DB%

ECHO ERRORLEVEL=%ERRORLEVEL%