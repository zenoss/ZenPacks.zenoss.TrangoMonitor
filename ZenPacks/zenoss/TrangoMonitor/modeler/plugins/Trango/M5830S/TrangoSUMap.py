######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

__doc__ = """TrangoSUMap
Gather SU information from Trango M583OS devices.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
    GetTableMap

class TrangoSUMap(SnmpPlugin):
    
    maptype = "TrangoSUMap"
    relname = "subscriberUnits"
    modname = "ZenPacks.zenoss.TrangoMonitor.TrangoSU"
    
    snmpGetTableMaps = (
        GetTableMap(
            'suInfoTable', '.1.3.6.1.4.1.5454.1.20.3.6.1', {
                '.1': 'id',
                '.2': 'mac',
                '.3': 'polling',
                '.4': 'peerGroup',
                '.5': 'cir',
                '.6': 'mir',
                '.7': 'ipAddr',
                '.8': 'remarks',
                '.9': 'hwVer',
                '.10': 'fwVer',
                '.11': 'fpgaVer',
                '.12': 'checksum',
                '.13': 'association',
                '.14': 'distance',
            }),
        )
    
    def pollingString(self, value):
        if value == 1: return "Regular"
        elif value == 5: return "Priority"
        return "Unknown"
    
    def peerGroupString(self, value):
        peerGroupMap = ("No Group", "Group 1", "Group 2", "Group 3", "Group 4",
            "Group 5", "Group 6", "Group 7", "Group 8", "Group 9", "Group A",
            "Group B", "Group C", "Group D", "Group E", "Group F")
        try:
            return peerGroupMap[value]
        except IndexError:
            return "Unknown"
    
    def associationString(self, value):
        if value == 0: return "Not Associated"
        elif value == 1: return "Associated"
        return "Unknown"
    
    
    def process(self, device, results, log):
        log.info("processing %s for device %s", self.name(), device.id)
        getdata, tabledata = results
        suTable = tabledata.get("suInfoTable")
        rm = self.relMap()
        for snmpindex, row in suTable.items():
            om = self.objectMap(row)
            om.snmpindex = snmpindex
            om.id = str(om.id)
            om.mac = self.asmac(om.mac)
            om.hwVer = self.asmac(om.hwVer)
            om.fpgaVer = self.asmac(om.fpgaVer)
            om.checksum = self.asmac(om.checksum)
            om.polling = self.pollingString(om.polling)
            om.peerGroup = self.peerGroupString(om.peerGroup)
            om.association = self.associationString(om.association)
            rm.append(om)
        return rm
