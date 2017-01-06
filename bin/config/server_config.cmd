:: auth server
set AUTH_SERVER_HOST=localhost
set AUTH_SERVER_PORT=9000

:: master server
set MASTER_SERVER_HOST=localhost
set MASTER_SERVER_QUEUE_PORT=5672
set MS_AUTH_QUEUE_NAME=ms-auth-pipe-XCXX
set MS_CLIENT_QUEUE_NAME=ms-client-pipe-XCXX

:: database
set DB_HOST_NAME=mongodb://localhost
set DB_PORT=27017
set MASTER_DB_NAME=shop7_test


set RES_FOLDER=%~dp0../data/res

set CATEGORY_MAPPING_FILENAME=ut/mapping.xml