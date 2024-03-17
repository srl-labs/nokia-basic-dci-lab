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
clabverter --stdout --naming non-prefixed --disableExpose true \
| kubectl apply -f -
```

## Misc

### Replace underscores in names

```
sed -ir 's/([a-zA-Z0-9]+)_dc/\1-dc/g' dci.clab.yml
```
