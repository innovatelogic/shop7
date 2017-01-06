@echo off

call %~dp0/config/server_config.cmd

set PYTHON="%python%"
set SCRIPT=""-u %~dp0/../src/server/launch.py --host %MASTER_SERVER_HOST% --res %RES_FOLDER% --mapping %CATEGORY_MAPPING_FILENAME%""
set MS_INFO=""--ms_auth_queue %MS_AUTH_QUEUE_NAME% --ms_client_queue %MS_CLIENT_QUEUE_NAME% --ms_queue_port %MASTER_SERVER_QUEUE_PORT%""
set DB_PARAMS=""--dbhost %DB_HOST_NAME% --dbport %DB_PORT% --dbname %MASTER_DB_NAME%""

python %SCRIPT% %MS_INFO% %DB_PARAMS% %*

ECHO ERRORLEVEL=%ERRORLEVEL%