# nokia-basic-dci-lab

A basic Datacenter Interconnect (DCI) lab for with leaf/spine switches powered by SR Linux and DC Gateway and P routers powered by Nokia 7750 SR OS.

In this lab, you will see two DC fabrics with VXLAN/EVPN and a WAN network that interconnects them with BGP-VPN. 

There are clients connected to some Leaf routers(see the topology below) in every site to test the connectivity and generate some in the fabric.

## Images & License

This lab requires containerized images of both SR Linux and SROS and a valid vSIM license for SROS.
SR Linux container image is automatically pulled from the public repository upon deploying the lab. (See the topology file)
SROS container image is available via a Nokia private repository, but can also be derived from an vSIM VM image via [VRNETLAB](https://containerlab.dev/manual/vrnetlab/#vrnetlab).

## Topology

![image](https://github.com/srl-labs/nokia-basic-dci-lab/assets/17744051/1f3d61a0-ae6a-42b2-b680-c282a6462d41)

## Deploy on containerlab

From within the cloned directory run:

```bash
sudo clab deploy -c
```

## Deploy on c9s

### Install clabernetes

```bash
helm upgrade --install --create-namespace --namespace c9s \
    clabernetes oci://ghcr.io/srl-labs/clabernetes/clabernetes
```

### Setup clabverter

```bash
alias clabverter='sudo docker run --user $(id -u) \
    -v /opt/nokia:/opt/nokia \
    -v $(pwd):/clabernetes/work --rm \
    ghcr.io/srl-labs/clabernetes/clabverter:latest'
```

### Run clabverter

```bash
clabverter --stdout --naming non-prefixed --disableExpose \
| kubectl apply -f -
```

## Client connectivity validation

### With containerlab

```bash
./netcheck.sh
```

### With c9s

Automated ping tests from client1 towards client2, client3 and client4 can be done with:

```bash
./netcheck-c9s.sh
```

The output will show the success or failure of the ping tests for each destination.

To run the ping tests manually, use the following command:

```bash
kubectl exec -it -n c9s-dci <pod-name-for-client1> -- docker exec -it client1-dc1 ping 10.0.0.4
```

## Cleanup

### Containerlab

```bash
sudo clab destroy -c
```

### c9s

```bash
kubectl delete namespace c9s-dci
```

If you wish to also uninstall the clabernetes:

```bash
helm uninstall -n c9s clabernetes && \
kubectl delete namespace c9s
```

## Misc

### Traffic capture with wireshark

```bash
pcapc9s.sh <host-with-kubectl> c9s-dci client4 eth1
```

### Replace underscores in names

```
sed -ir 's/([a-zA-Z0-9]+)_dc/\1-dc/g' dci.clab.yml
```
