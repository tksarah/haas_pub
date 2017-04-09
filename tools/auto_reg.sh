#!/bin/bash

IPADDR="192.168.175.202"
HAAS_PATH="haas"

URL="http://$IPADDR/$HAAS_PATH/create.cgi"
TYPE="ansible-2"

for USER in `cat users.txt`
  do
    echo -n "For $USER Building ... "
    curl $URL -X POST -d "name=$USER" -d "type=$TYPE" >& /dev/null
    sleep 10
    echo "Finished."
  done

