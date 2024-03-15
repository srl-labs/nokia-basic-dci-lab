#!/bin/bash
# run as bash check-connectivity.sh all

CASE=$1

if [ -z "$CASE" ]; then
    CASE="all"
fi

ping_test() {
    sudo docker exec clab-dci-leaf1_dc1 ip netns exec srbase-ip-vrf101 ping -c 1 -w 1 $1 > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "+ \e[32mPing from leaf1 (dc1) to $2 ($1) was successful.\e[0m"
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
    echo "Running pings from leaf1 (dc1)"
    # ping all cases and print the results that pass and don't pass
    ping_test 10.0.0.12 "leaf2 (dc1)"
    ping_test 10.0.0.13 "leaf3 (dc1)"
    ping_test 10.0.0.14 "leaf4 (dc1)"
    echo
    ping_test 20.0.0.12 "leaf2 (dc2)"
    ping_test 20.0.0.13 "leaf3 (dc2)"
    ping_test 20.0.0.14 "leaf4 (dc2)"
    exit 0
fi

echo "Invalid mode. Please use one of the following modes: all, dc1 or dc2"
exit 1