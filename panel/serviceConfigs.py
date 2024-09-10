#CDN1
serviceLocalCDN = [
    (
      "srl_nokia-network-instance:network-instance[name=subnetA]",
      {
          "admin-state": "enable",
          "bridge-table": {
            "mac-learning": {
              "admin-state": "enable"
            },
          },
          "interface": [
            {
              "name": "ethernet-1/1.0",
            },
            {
              "name": "irb1.1",
            }
          ],
          "protocols": {
            "bgp-evpn": {
              "srl_nokia-bgp-evpn:bgp-instance": [
                {
                  "admin-state": "enable",
                  "ecmp": 8,
                  "encapsulation-type": "vxlan",
                  "evi": 1,
                  "id": 1,
                  "vxlan-interface": "vxlan1.1"
                }
              ]
            },
            "srl_nokia-bgp-vpn:bgp-vpn": {
              "bgp-instance": [
                {
                  "id": 1,
                  "route-target": {
                    "export-rt": "target:65501:1",
                    "import-rt": "target:65501:1"
                  }
                }
              ]
            },
          },
          "type": "srl_nokia-network-instance:mac-vrf",
          "vxlan-interface": [
            {
              "name": "vxlan1.1"
            }
          ]
      }
    )
]

#CDN2 and Internet
serviceRemote = [
    (
      "srl_nokia-network-instance:network-instance[name=subnetB]",
      {
          "admin-state": "enable",
          "bridge-table": {
            "mac-learning": {
              "admin-state": "enable"
            },
          },
          "interface": [
            {
              "name": "ethernet-1/1.0",
            },
            {
              "name": "irb1.1",
            }
          ],
          "protocols": {
            "bgp-evpn": {
              "srl_nokia-bgp-evpn:bgp-instance": [
                {
                  "admin-state": "enable",
                  "ecmp": 8,
                  "encapsulation-type": "vxlan",
                  "evi": 1,
                  "id": 1,
                  "vxlan-interface": "vxlan1.1"
                }
              ]
            },
            "srl_nokia-bgp-vpn:bgp-vpn": {
              "bgp-instance": [
                {
                  "id": 1,
                  "route-target": {
                    "export-rt": "target:65501:1",
                    "import-rt": "target:65501:1"
                  }
                }
              ]
            },
          },
          "type": "srl_nokia-network-instance:mac-vrf",
          "vxlan-interface": [
            {
              "name": "vxlan1.1"
            }
          ]
      }
    )
]