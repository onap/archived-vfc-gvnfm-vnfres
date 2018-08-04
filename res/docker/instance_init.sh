#!/bin/bash

function start_redis_server {
    redis-server &
}

function start_mysql {
    service mysql start
    sleep 1
}

function create_database {
    cd /service/vfc/gvnfm/vnfres/res/assembly/bin
    if [ ! -f dbexist.txt ]; then
        echo 1 > dbexist.txt
        bash initDB.sh root $MYSQL_ROOT_PASSWORD 3306 127.0.0.1
    fi
    cd /service
}

start_redis_server
start_mysql
create_database