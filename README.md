# nokia-basic-dci-lab

A basic Datacenter Interconnect (DCI) lab for with leaf/spine switches powered by SR Linux and DC Gateway and P routers powered by Nokia 7750 SR OS.

## Deploy on c9s

Setting up additional volume mount to get access to the license file

```
alias clabverter='sudo docker run --user $(id -u) \
    -v /opt/nokia:/opt/nokia \
    -v $(pwd):/clabernetes/work --rm \
    ghcr.io/srl-labs/clabernetes/clabverter:latest'
```

and then run

```
clabverter --stdout --naming non-prefixed --disableExpose \
| kubectl apply -f -
```

## Ping tests

### Automated

`bash ./netcheck-c9s.sh`

### Manual

`k exec -it -n c9s-dci client1-dc1-77cc46c75f-txnc8 -- docker exec -it client1-dc1 ping 10.0.0.4`

## Misc

### Replace underscores in names

```
sed -ir 's/([a-zA-Z0-9]+)_dc/\1-dc/g' dci.clab.yml
```
