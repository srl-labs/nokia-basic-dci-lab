#Flask library - Web application
from flask import Flask, render_template, request, redirect, url_for
#YAML library - Reading yaml files
import yaml
#pyGNMI - To configure and retrieve state from the routers
from pygnmi.client import gNMIclient
#Services file
from serviceConfigs import *
#System libraries
import re

#Hosts YAML file
nameHostsFile = "hosts.yaml"
hosts = []

#Function to read YAML file
def readingHosts():
  with open(nameHostsFile, 'r') as file:
    hostsFile = yaml.safe_load(file)
  return hostsFile

#Function to do a GNMI Get
def gnmiGet(host, port, username, password, path, insecureGNMI, skipVerifyGNMI):
   with gNMIclient(target=(host, port), username=username, password=password, insecure=insecureGNMI, skip_verify=skipVerifyGNMI) as gc:
      result = gc.get(path=[path])
      return result

#Function to retrieve the services
def getServices(hosts):
  cdn = False #Leaf4-DC1
  redundancy = False #Leaf1-DC2
  internet = False #Leaf4-DC2

  for host in hosts:

    if host["mgmt-ip"] == "172.0.200.124": #Leaf4-DC1
      r = gnmiGet(host['mgmt-ip'], host['grpc-port'], host['username'], host['password'], "/network-instance[name=subnetA]/admin-state", host["insecure"], host["skipVerify"])
      if len(r['notification'][0]) > 4:
        if r['notification'][0]['update'][0]['val'] == "enable":
          cdn = True

    if host["mgmt-ip"] == "172.0.200.221": #Leaf1-DC2
      r = gnmiGet(host['mgmt-ip'], host['grpc-port'], host['username'], host['password'], "/network-instance[name=subnetB]/admin-state", host["insecure"], host["skipVerify"])
      if len(r['notification'][0]) > 4:
        if r['notification'][0]['update'][0]['val'] == "enable":
          redundancy = True

    if host["mgmt-ip"] == "172.0.200.224": #Leaf4-DC2
      r = gnmiGet(host['mgmt-ip'], host['grpc-port'], host['username'], host['password'], "/network-instance[name=subnetB]/admin-state", host["insecure"], host["skipVerify"])
      if len(r['notification'][0]) > 4:
        if r['notification'][0]['update'][0]['val'] == "enable":
          internet = True  

  return cdn, redundancy, internet

#Function to retrieve interface status
def getInterfaces(host, dataModel):
  # Using OpenConfig Data Model:
  if dataModel == "openconfig":
    print("openconfig")
  # Using Nokia SR OS Data Model:
  else:
    if dataModel == "sros":
      r = gnmiGet(host['mgmt-ip'], host['grpc-port'], host['username'], host['password'], "/state/router/interface[interface-name=*]/oper-state", host["insecure"], host["skipVerify"])
      return r
  # Using Nokia SR Linux Data Model:
    if dataModel == "srl":
      r = gnmiGet(host['mgmt-ip'], host['grpc-port'], host['username'], host['password'], "/interface[name=*]/admin-state", host["insecure"], host["skipVerify"])
      return r

def getNetworkInterfaces(hosts):
  interfaceList = []
  for host in hosts:
    hostMgmtIP = host["mgmt-ip"]
    hostPort = host["grpc-port"]
    hostUser = host["username"]
    hostPass = host["password"]
    hostSystemName = host["system-name"]
    hostOS = host["nos"]
    hostInsecure = host["insecure"]
    hostSkipVerify = host["skipVerify"]
    outputGetIfStatus = getInterfaces(host, hostOS)
    interfaceName = ""
    interfaceStatus = ""

    if hostOS == "sros":
      interfaces = outputGetIfStatus['notification'][0]['update']
      for intf in interfaces:
        interfaceName = re.search(r'interface\[interface-name=(.*?)\]', intf['path']).group(1)
        interfaceStatus = intf['val']
        if interfaceStatus == "up":
          interfaceStatus = "enable"
        if interfaceStatus == "down":
          interfaceStatus = "disable"
        interfaceList.append({"hostName": hostSystemName, "hostIP": hostMgmtIP, "hostPort": hostPort, "hostUser": hostUser, "hostPass": hostPass, "hostOS": hostOS, "interfaceName": interfaceName, "interfaceStatus": interfaceStatus, "insecure": hostInsecure, "skipVerify": hostSkipVerify})
    
    if hostOS == "srl":
      interfaces = outputGetIfStatus['notification'][0]['update'][0]['val']['srl_nokia-interfaces:interface']
      for intf in interfaces:
        interfaceName = intf['name']
        interfaceStatus = intf['admin-state']
        interfaceList.append({"hostName": hostSystemName, "hostIP": hostMgmtIP, "hostPort": hostPort, "hostUser": hostUser, "hostPass": hostPass, "hostOS": hostOS, "interfaceName": interfaceName, "interfaceStatus": interfaceStatus, "insecure": hostInsecure, "skipVerify": hostSkipVerify})
  
  return interfaceList

#Function to do a GNMI Set Delete
def gnmiDelete(host, port, username, password, d, insecureGNMI, skipVerifyGNMI):
  with gNMIclient(target=(host, port), username=username, password=password, insecure=insecureGNMI, skip_verify=skipVerifyGNMI) as gc:
    result = gc.set(delete=d)
    print(result)
    return result

#Function to do a GNMI Set Update
def gnmiSet(host, port, username, password, path, leafName, value, insecureGNMI, skipVerifyGNMI):
  with gNMIclient(target=(host, port), username=username, password=password, insecure=insecureGNMI, skip_verify=skipVerifyGNMI) as gc:
    u = [(path, {leafName: value},)]
    result = gc.set(update=u)
    return result

#Function to do a GNMI Set Update from a file
def gnmiSetFromFile(host, port, username, password, u, insecureGNMI, skipVerifyGNMI):
  with gNMIclient(target=(host, port), username=username, password=password, insecure=insecureGNMI, skip_verify=skipVerifyGNMI) as gc:
    result = gc.set(update=u, encoding='json_ietf')
    return result

#Function to set the services
def setServices(hosts, cdn, redundancy, internet):
  for host in hosts:

    #Connection to CDN#1
    if host["system-name"] == "leaf4-dc1":
      if cdn == "True":
        gnmiSetFromFile(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], serviceLocalCDN, host["insecure"], host["skipVerify"])
      else:
        gnmiDelete(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], ["network-instance[name=subnetA]"], host["insecure"], host["skipVerify"])

    #Connection to CDN#2
    if host["system-name"] == "leaf1-dc2":
      if redundancy == "True":
        gnmiSetFromFile(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], serviceRemote, host["insecure"], host["skipVerify"])
      else:
        gnmiDelete(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], ["network-instance[name=subnetB]"], host["insecure"], host["skipVerify"])   

    #Connection to Internet
    if host["system-name"] == "leaf4-dc2":
      if internet == "True":
        gnmiSetFromFile(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], serviceRemote, host["insecure"], host["skipVerify"])
      else:
        gnmiDelete(host["mgmt-ip"], host["grpc-port"], host["username"], host["password"], ["network-instance[name=subnetB]"], host["insecure"], host["skipVerify"])

#Function to set interface admin-state
def setInterfaceAdminState(host, port, username, password, dataModel, interfaceName, status, insecureGNMI, skipVerifyGNMI):
  if dataModel == "srl":
    return gnmiSet(host, port, username, password, f"/interface[name={interfaceName}]", "admin-state", status, insecureGNMI, skipVerifyGNMI)
  if dataModel == "sros":
    return gnmiSet(host, port, username, password, f"/configure/router[router-name=Base]/interface[interface-name={interfaceName}]", "admin-state", status, insecureGNMI, skipVerifyGNMI)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():  
  #Reading yaml file
  hostsFile = readingHosts()
  #Saving yaml information in hosts var
  hosts = hostsFile["routers"]
  #Printing the information
  #print(hosts)

  #Retrieving the interfaces from each router in the yaml file
  networkInterfaces = getNetworkInterfaces(hosts)

  #Saving the importan info to show in the web app
  routersAndInterfaces = []
  for auxNetworkInterfaces in networkInterfaces:
    auxRtrName = auxNetworkInterfaces["hostName"]
    auxItfName = auxNetworkInterfaces["interfaceName"]
    auxItfStatus = auxNetworkInterfaces["interfaceStatus"]
    routersAndInterfaces.append(f"{auxRtrName}, {auxItfName}, {auxItfStatus}")
  
  #Retrieving the services status from each leaf
  cdn, redundancy, internet = getServices(hosts)

  #If POST Request
  if request.method == 'POST':

    #If action is toggleInterface we need to toggle the interface admin-status enable <-> disable
    if request.form['action'] == 'toggleInterface':
      #What interface? response:
      selectedInterface = request.form.get('interface')
      print(selectedInterface)
      counter = 0
      for auxRtrAndItfs in routersAndInterfaces:
        if selectedInterface == auxRtrAndItfs:
          nextStatus = ""
          if networkInterfaces[counter]["interfaceStatus"] == "disable":
            nextStatus = "enable"
          else:
            nextStatus = "disable"
          setInterfaceAdminState(networkInterfaces[counter]["hostIP"], networkInterfaces[counter]["hostPort"], networkInterfaces[counter]["hostUser"], networkInterfaces[counter]["hostPass"], networkInterfaces[counter]["hostOS"], networkInterfaces[counter]["interfaceName"], nextStatus, networkInterfaces[counter]["insecure"], networkInterfaces[counter]["skipVerify"])
        counter = counter + 1
      
      return redirect(url_for('index'))

    #If action is setServices:
    if request.form['action'] == 'setServices':
      #Retrieving the desired status
      cdnService = request.form.get('cdn')
      redundancyCDNService = request.form.get('redundancy')
      internetService = request.form.get('internet')
      #Setting the desired service status
      setServices(hosts, cdnService, redundancyCDNService, internetService)
      return redirect(url_for('index'))

  return render_template('index.html', routersAndInterfaces=routersAndInterfaces, cdn=cdn, redundancy=redundancy, internet=internet)

if __name__ == '__main__':
    app.run(debug=True)
