##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """TrangoInterfaceMap
Gather information on Trango M583OS interfaces.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class TrangoInterfaceMap(SnmpPlugin):
    maptype = "TrangoInterfaceMap"
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.5454.1.20.1.2.0': 'apsysDeviceId',
        '.1.3.6.1.4.1.5454.1.20.1.8.0': 'apsysIPAddr',
        '.1.3.6.1.4.1.5454.1.20.1.9.0': 'apsysSubnet',
        })

    def process(self, device, results, log):
        log.info("processing %s for device %s", self.name(), device.id)
        getdata, tabledata = results
        if getdata['apsysIPAddr'] is None: return None
        maskBits = self.maskToBits(getdata['apsysSubnet'])
        rm = self.relMap()
        om = self.objectMap()
        om.id = "ethernet"
        om.ifindex = "1"
        om.title = "ethernet"
        om.type = "trangoApEthernet"
        om.adminStatus = 1
        om.operStatus = 1
        om.speed = 100000000
        om.mtu = 1500
        ip = getdata['apsysIPAddr'] + "/" + str(maskBits)
        om.setIpAddresses = [ip,]
        om.macaddress = self.asmac(getdata['apsysDeviceId'])
        rm.append(om)
        
        return rm
