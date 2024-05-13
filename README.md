# nokia-basic-dci-lab

A basic Datacenter Interconnect (DCI) lab for with leaf/spine switches powered by SR Linux and DC Gateway and P routers powered by Nokia 7750 SR OS.

## Topology

![image](https://github.com/srl-labs/nokia-basic-dci-lab/assets/17744051/f16f45d6-a4fd-4857-9ae9-864a998c86fd)

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

## Basic Ping Test

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

### With containerlab

```bash
./netcheck.sh
```

## L3 DCI Connectivity Validation

## L2 DCI Connectivity Validation

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
