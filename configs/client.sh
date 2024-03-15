#!/bin/bash

# client id
DC_ID=$1
ID=$2

if [ "$DC_ID" = "dc1" ]; then
    FIRST_OCTET=10
elif [ "$DC_ID" = "dc2" ]; then
    FIRST_OCTET=20
else
    echo "Invalid DC_ID"
fi

###### eth1 ######
ip addr add ${FIRST_OCTET}.0.0.${ID}/30 dev eth1
ip link set dev eth1 address aa:c1:ab:${FIRST_OCTET}:00:0${ID}
