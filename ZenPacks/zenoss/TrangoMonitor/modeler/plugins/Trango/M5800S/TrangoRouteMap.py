##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """TrangoRouteMap
Gather Trango routing information.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class TrangoRouteMap(SnmpPlugin):
    maptype = "TrangoInterfaceMap"
    compname = "os"
    relname = "routes"
    modname = "Products.ZenModel.IpRouteEntry"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.5454.1.10.1.9.0': 'apsysSubnet',
        '.1.3.6.1.4.1.5454.1.10.1.10.0': 'apsysDefaultGateway',
        })

    def process(self, device, results, log):
        log.info("processing %s for device %s", self.name(), device.id)
        getdata, tabledata = results
        if getdata['apsysDefaultGateway'] is None: return None
        dg = getdata['apsysDefaultGateway']
        maskBits = self.maskToBits(getdata['apsysSubnet'])
        rm = self.relMap()
        om = self.objectMap()
        om.id = dg + "_" + str(maskBits)
        om.setInterfaceIndex = "1"
        om.setNextHopIp = dg
        om.routemask = maskBits
        om.routetype = 'indirect'
        om.routeproto = 'local'
        om.routemask = self.maskToBits(getdata['apsysSubnet'])
        om.setTarget = dg + "/" + str(maskBits)
        rm.append(om)
        
        return rm
