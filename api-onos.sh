#!/bin/bash

#2 ways
echo "$(curl -u onos:rocks -X GET --header 'Accept: application/json' 'http://localhost:8181/onos/v1/links')" > links.json
sleep 1
echo "$(curl -u onos:rocks -X GET --header 'Accept: application/json' 'http://localhost:8181/onos/v1/hosts')" > hosts.json
sleep 1
echo "$(curl -u onos:rocks -X GET --header 'Accept: application/json' 'http://localhost:8181/onos/v1/devices')" > devices.json
#curl -u onos:rocks -o output.json http://localhost:8181/onos/v1/links

exit 0


