# nokia-basic-dci-lab

## Clabverter

Setting up additional volume mount to get access to the license file

```
alias clabverter='sudo docker run --user $(id -u) \
    -v /opt/nokia:/opt/nokia \
    -v $(pwd):/clabernetes/work --rm \
    ghcr.io/srl-labs/clabernetes/clabverter:latest'
```

## Replace underscores

```
sed -ir 's/([a-zA-Z0-9]+)_dc/\1-dc/g' dci.clab.yml
```
