######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap

class TrangoDeviceMap(SnmpPlugin):
    """Maps device level information from Trango access points
    """
    
    maptype = "TrangoDeviceMap"
    
    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.5454.1.10.1.1.1.0': 'sysHW',
        '.1.3.6.1.4.1.5454.1.10.1.1.2.0': 'sysFW',
        '.1.3.6.1.4.1.5454.1.10.1.1.3.0': 'sysFPGA',
        '.1.3.6.1.4.1.5454.1.10.1.1.4.0': 'sysChecksum',
        '.1.3.6.1.4.1.5454.1.10.1.2.0': 'sysDeviceId',
        '.1.3.6.1.4.1.5454.1.10.1.3.0': 'sysBaseId',
        '.1.3.6.1.4.1.5454.1.10.1.4.0': 'sysAPId',
        '.1.3.6.1.4.1.5454.1.10.1.5.0': 'sysDefOpMode',
        '.1.3.6.1.4.1.5454.1.10.1.13.1.0': 'sysBlockBroadcastMulticast',
        '.1.3.6.1.4.1.5454.1.10.1.13.2.0': 'sysSUtoSU',
        '.1.3.6.1.4.1.5454.1.10.1.13.4.0': 'sysTFTPD',
        '.1.3.6.1.4.1.5454.1.10.1.13.5.0': 'sysHTTPD',
        '.1.3.6.1.4.1.5454.1.10.1.14.0': 'sysMIRThreshold',
        
        '.1.3.6.1.4.1.5454.1.10.2.1.0': 'rfActiveChannel',
        '.1.3.6.1.4.1.5454.1.10.2.2.0': 'rfActivePolarization',
        
        '.1.3.6.1.4.1.5454.1.10.2.4.1.0': 'ismTxPowerMax',
        '.1.3.6.1.4.1.5454.1.10.2.4.2.0': 'ismTxPowerMin',
        '.1.3.6.1.4.1.5454.1.10.2.4.3.0': 'ismTxPower',
        '.1.3.6.1.4.1.5454.1.10.2.4.4.0': 'ismServiceRadius',
        '.1.3.6.1.4.1.5454.1.10.2.4.5.0': 'ismRxThreshold',
        '.1.3.6.1.4.1.5454.1.10.2.4.6.0': 'ismTargetRSSI',
        
        '.1.3.6.1.4.1.5454.1.10.2.5.1.0': 'uniiTxPowerMax',
        '.1.3.6.1.4.1.5454.1.10.2.5.2.0': 'uniiTxPowerMin',
        '.1.3.6.1.4.1.5454.1.10.2.5.3.0': 'uniiTxPower',
        '.1.3.6.1.4.1.5454.1.10.2.5.4.0': 'uniiServiceRadius',
        '.1.3.6.1.4.1.5454.1.10.2.5.5.0': 'uniiRxThreshold',
        '.1.3.6.1.4.1.5454.1.10.2.5.6.0': 'uniiTargetRSSI',
        })
    
    def opModeString(self, value):
        if value == 0: return "Off"
        elif value == 1: return "On"
        return "Unknown"
    
    def blockString(self, value):
        if value == 0: return "Passed"
        elif value == 1: return "Blocked"
        return "Unknown"
    
    def enabledString(self, value):
        if value == 0: return "Disabled"
        elif value == 1: return "Enabled"
        return "Unknown"
    
    def mirThresholdString(self, value):
        if value == 0:
            return "Disabled"
        return "%dMbps" % value
    
    def serviceRadiusString(self, value):
        if value == 2: return "2 Miles"
        elif value == 3: return "3 Miles"
        elif value == 4: return "4 Miles"
        elif value == 10: return "10 Miles"
        elif value == 20: return "30 Miles:"
        return "Unknown"


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['sysHW'] is None: return None
        om = self.objectMap(getdata)
        om.setOSProductKey = om.sysFW
        om.sysHW = self.asmac(om.sysHW)
        om.sysFPGA = self.asmac(om.sysFPGA)
        om.sysChecksum = self.asmac(om.sysChecksum)
        om.sysDeviceId = self.asmac(om.sysDeviceId)
        om.sysDefOpMode = self.opModeString(om.sysDefOpMode)
        om.sysBlockBroadcastMulticast = self.blockString(
            om.sysBlockBroadcastMulticast)
        om.sysSUtoSU = self.enabledString(om.sysSUtoSU)
        om.sysTFTPD = self.enabledString(om.sysTFTPD)
        om.sysHTTPD = self.enabledString(om.sysHTTPD)
        om.sysMIRThreshold = self.mirThresholdString(om.sysMIRThreshold)
        om.ismServiceRadius = self.serviceRadiusString(om.ismServiceRadius)
        om.uniiServiceRadius = self.serviceRadiusString(om.uniiServiceRadius)
        return om
