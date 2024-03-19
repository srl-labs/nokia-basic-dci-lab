#!/bin/bash

# client id
DC_ID=$1
ID=$2

if [ "$DC_ID" = "dc1" ]; then
    FIRST_OCTET=10
    REMOTE_OCTET=20
elif [ "$DC_ID" = "dc2" ]; then
    FIRST_OCTET=20
    REMOTE_OCTET=10
else
    echo "Invalid DC_ID"
fi

###### eth1 ######
ip addr add ${FIRST_OCTET}.0.0.${ID}/24 dev eth1
ip link set dev eth1 address aa:c1:ab:${FIRST_OCTET}:00:0${ID}

# a route towards the local DC clients via the anycast gw
ip route add ${FIRST_OCTET}.0.0.0/24 via ${FIRST_OCTET}.0.0.254
# a route towards the leaf loopbacks in the l3 vrf
ip route add ${FIRST_OCTET}.1.0.0/24 via ${FIRST_OCTET}.0.0.254

# a route towards the remote DC clients via the anycast gw
ip route add ${REMOTE_OCTET}.0.0.0/24 via ${FIRST_OCTET}.0.0.254
# a route towards the remote leafs loopbacks in the l3 vrf
ip route add ${REMOTE_OCTET}.1.0.0/24 via ${FIRST_OCTET}.0.0.254

# set PS1
echo "export PS1='\[\033[0;32m\]\u@\h:\[\033[36m\]\W\[\033[0m\] \$ '" > /root/.bashrc
chmod +x /root/.bashrc
. /root/.bashrc