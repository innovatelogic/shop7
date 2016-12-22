@echo off

call %~dp0/config/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0..\src\server\auth\launch.py --host %AUTH_SERVER_HOST% --port %AUTH_SERVER_PORT%""
set MSINFO=""--mshost %MASTER_SERVER_HOST% --ms_auth_queue %MS_AUTH_QUEUE_NAME% --ms_queue_port %MASTER_SERVER_QUEUE_PORT%"" 

python %SCRIPT% %MSINFO% %*

ECHO ERRORLEVEL=%ERRORLEVEL%