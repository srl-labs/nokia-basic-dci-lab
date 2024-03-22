#!/bin/bash
# example usage: ./netcheck.sh

CASE=$1

if [ -z "$CASE" ]; then
    CASE="all"
fi

ping_test() {
    sudo docker exec clab-dci-client1-dc1 ping -c 1 -w 1 $1 &> /dev/null
    if [ $? -eq 0 ]; then
        echo -e "+ \e[32mPing from leaf1 (dc1) to $2 ($1) was successful.\e[0m"
    else
        echo -e "- \e[31mPing to $1 ($2) failed.\e[0m"
    fi
}

if [ "$CASE" == "dc1" ]; then
    ping_test 10.0.0.4 "client2/dc1"
    exit 0
fi

if [ "$CASE" == "dc2" ]; then
    ping_test 20.0.0.1 "client3/dc2"
    ping_test 20.0.0.4 "client4/dc2"
    exit 0
fi

if [ "$CASE" == "all" ]; then
    echo "Running pings from client1/dc1 (10.0.0.1)"
    # ping all cases and print the results that pass and don't pass
    ping_test 10.0.0.4 "client2/dc1"
    echo
    ping_test 20.0.0.1 "client3/dc2"
    ping_test 20.0.0.4 "client4/dc2"
    exit 0
fi

echo "Invalid mode. Please use one of the following modes: all, dc1 or dc2"
exit 1