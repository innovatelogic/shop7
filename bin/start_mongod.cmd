@echo off

set CONFIG_FILE="%~dp0mongod.conf"

mongod --config %CONFIG_FILE%

ECHO ERRORLEVEL=%ERRORLEVEL%