set -eu

startTraffic-all() {
    echo "Starting traffic between customer and: Local CDN, Remote CDN, Internet"
    sudo docker exec clab-dci-client2-dc1 iperf3 -s -B 10.0.0.4 -p 5202 &
    sudo docker exec clab-dci-client3-dc2 iperf3 -s -B 20.0.0.1 -p 5203 &
    sudo docker exec clab-dci-client4-dc2 iperf3 -s -B 20.0.0.4 -p 5204 &
    sudo docker exec clab-dci-client1-dc1 /bin/bash -c 'while true; do iperf3 -c 10.0.0.4 -t 10000 -i 1 -p 5202 -B 10.0.0.1 -P 8 -b 200K -M 1000; if [ $? -ne 0 ]; then echo "Failed, trying again in 5 seconds..."; sleep 5; fi; done' &
    sudo docker exec clab-dci-client1-dc1 /bin/bash -c 'while true; do iperf3 -c 20.0.0.1 -t 10000 -i 1 -p 5203 -B 10.0.0.1 -P 8 -b 200K -M 1000; if [ $? -ne 0 ]; then echo "Failed, trying again in 5 seconds..."; sleep 5; fi; done' &
    sudo docker exec clab-dci-client1-dc1 /bin/bash -c 'while true; do iperf3 -c 20.0.0.4 -t 10000 -i 1 -p 5204 -B 10.0.0.1 -P 8 -b 200K -M 1000; if [ $? -ne 0 ]; then echo "Failed, trying again in 5 seconds..."; sleep 5; fi; done' &
}   

stopTraffic-all() {
    echo "Stopping traffic between customer and: Local CDN, Remote CDN, Internet"
    sudo docker exec clab-dci-client1-dc1 pkill -f "iperf3"
    sudo docker exec clab-dci-client1-dc1 pkill -f "while true"
    sudo docker exec clab-dci-client2-dc1 pkill -f "iperf3"
    sudo docker exec clab-dci-client3-dc2 pkill -f "iperf3"
    sudo docker exec clab-dci-client4-dc2 pkill -f "iperf3"
}

# start traffic
if [ $1 == "start" ]; then
    if [ $2 == "all" ]; then
        startTraffic-all
    fi
fi

# stop traffic
if [ $1 == "stop" ]; then
    if [ $2 == "all" ]; then
        stopTraffic-all
    fi
fi