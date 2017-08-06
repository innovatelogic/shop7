@echo off

set CONFIG_FILE="%~dp0/config/mongod.conf"

mongod --config %CONFIG_FILE%

ECHO ERRORLEVEL=%ERRORLEVEL%