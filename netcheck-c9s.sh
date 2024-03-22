#!/bin/bash
# example usage: ./netcheck-c9s.sh

CASE=$1

NS=c9s-dci
POD_SHORTNAME=client1-dc1

# retrieve the full pod name based on its short name
POD=$(kubectl -n $NS get pods | grep ^$POD_SHORTNAME | awk '{print $1}')

if [ -z "$CASE" ]; then
    CASE="all"
fi

ping_test() {
    kubectl exec -it -n $NS $POD -- docker exec -it $POD_SHORTNAME ping -c 1 -w 2 $1 &> /dev/null
    if [ $? -eq 0 ]; then
        echo -e "+ \e[32mPing from client1/dc1 to $2 ($1) was successful.\e[0m"
    else
        echo -e "- \e[31mPing to $1 ($2) failed.\e[0m"
    fi
}

if [ "$CASE" == "dc1" ]; then
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 10.0.0.12
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 10.0.0.13
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 10.0.0.14
    exit 0
fi

if [ "$CASE" == "dc2" ]; then
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 20.0.0.12
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 20.0.0.13
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 20.0.0.14
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