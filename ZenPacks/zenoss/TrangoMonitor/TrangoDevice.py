######################################################################
#
# Copyright 2008 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class TrangoDevice(Device):
    "A Trango device"
    
    sysHW = ""
    sysFW = ""
    sysFPGA = ""
    sysChecksum = ""
    sysDeviceId = ""
    sysBaseId = None
    sysAPId = None
    sysDefOpMode = ""
    sysBlockBroadcastMulticast = None
    sysSUtoSU = None
    sysTFTPD = None
    sysHTTPD = None
    sysMIRThreshold = ""
    
    rfActiveChannel = None
    rfActivePolarization = ""
    
    ismTxPowerMax = None
    ismTxPowerMin = None
    ismTxPower = None
    ismServiceRadius = ""
    ismRxThreshold = None
    ismTargetRSSI = None
    
    uniiTxPowerMax = None
    uniiTxPowerMin = None
    uniiTxPower = None
    uniiServiceRadius = ""
    uniiRxThreshold = None
    uniiTargetRSSI = None
    
    _properties = Device._properties + (
        {'id':'sysHW', 'type':'string', 'mode':'w'},
        {'id':'sysFW', 'type':'string', 'mode':'w'},
        {'id':'sysFPGA', 'type':'string', 'mode':'w'},
        {'id':'sysChecksum', 'type':'string', 'mode':'w'},
        {'id':'sysDeviceId', 'type':'string', 'mode':'w'},
        {'id':'sysBaseId', 'type':'int', 'mode':'w'},
        {'id':'sysAPId', 'type':'int', 'mode':'w'},
        {'id':'sysDefOpMode', 'type':'string', 'mode':'w'},
        {'id':'sysBlockBroadcastMulticast', 'type':'boolean', 'mode':'w'},
        {'id':'sysSUtoSU', 'type':'boolean', 'mode':'w'},
        {'id':'sysTFTPD', 'type':'boolean', 'mode':'w'},
        {'id':'sysHTTPD', 'type':'boolean', 'mode':'w'},
        {'id':'sysMIRThreshold', 'type':'string', 'mode':'w'},
        
        {'id':'rfActiveChannel', 'type':'int', 'mode':'w'},
        {'id':'rfActivePolarization', 'type':'string', 'mode':'w'},
        
        {'id':'ismTxPowerMax', 'type':'int', 'mode':'w'},
        {'id':'ismTxPowerMin', 'type':'int', 'mode':'w'},
        {'id':'ismTxPower', 'type':'int', 'mode':'w'},
        {'id':'ismServiceRadius', 'type':'string', 'mode':'w'},
        {'id':'ismRxThreshold', 'type':'int', 'mode':'w'},
        {'id':'ismTargetRSSI', 'type':'int', 'mode':'w'},
        
        {'id':'uniiTxPowerMax', 'type':'int', 'mode':'w'},
        {'id':'uniiTxPowerMin', 'type':'int', 'mode':'w'},
        {'id':'uniiTxPower', 'type':'int', 'mode':'w'},
        {'id':'uniiServiceRadius', 'type':'string', 'mode':'w'},
        {'id':'uniiRxThreshold', 'type':'int', 'mode':'w'},
        {'id':'uniiTargetRSSI', 'type':'int', 'mode':'w'},
        )

    _relations = Device._relations + (
        ('subscriberUnits', ToManyCont(ToOne,
            'ZenPacks.zenoss.TrangoMonitor.TrangoSU', 'accessPoint')),
        )
    
    
    factory_type_information = deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2,
           { 'id'              : 'trangoDeviceDetail'
           , 'name'            : 'Wireless'
           , 'action'          : 'trangoDeviceDetail'
           , 'permissions'     : (ZEN_VIEW, ) },
           )
    factory_type_information[0]['actions'] = custom_actions


    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


    def sysBaseIdString(self):
        if self.sysBaseId is not None:
            return str(self.sysBaseId)
        return "Unknown"
    
    def sysAPIdString(self):
        if self.sysAPId is not None:
            return str(self.sysAPId)
        return "Unknown"
    
    def rfActiveChannelString(self):
        if self.rfActiveChannel is not None:
            return str(self.rfActiveChannel)
        return "Unknown"

    def ismTxPowerRangeString(self):
        if self.ismTxPowerMin is not None and self.ismTxPowerMax is not None:
            return "%d to %ddBm" % (self.ismTxPowerMin, self.ismTxPowerMax)
        return "Unknown"
    
    def ismTxPowerString(self):
        if self.ismTxPower is not None:
            return "%ddBm" % self.ismTxPower
        return "Unknown"
    
    def ismRxString(self):
        if self.ismRxThreshold is not None and self.ismTargetRSSI is not None:
            return "%d / %ddBm" % (self.ismRxThreshold, self.ismTargetRSSI)
        return "Unknown"
    
    def ismRxThresholdString(self):
        if self.ismRxThreshold is not None:
            return "%ddBm" % self.ismRxThreshold
        return "Unknown"
    
    def ismTargetRSSIString(self):
        if self.ismTargetRSSI is not None:
            return "%ddBm" % self.ismTargetRSSI
        return "Unknown"
    
    def uniiTxPowerRangeString(self):
        if self.uniiTxPowerMin is not None and self.uniiTxPowerMax is not None:
            return "%d to %ddBm" % (self.uniiTxPowerMin, self.uniiTxPowerMax)
        return "Unknown"

    def uniiTxPowerString(self):
        if self.uniiTxPower is not None:
            return "%ddBm" % self.uniiTxPower
        return "Unknown"

    def uniiRxString(self):
        if self.uniiRxThreshold is not None and self.uniiTargetRSSI is not None:
            return "%d / %ddBm" % (self.uniiRxThreshold, self.uniiTargetRSSI)
        return "Unknown"

    def uniiRxThresholdString(self):
        if self.uniiRxThreshold is not None:
            return "%ddBm" % self.uniiRxThreshold
        return "Unknown"

    def uniiTargetRSSIString(self):
        if self.uniiTargetRSSI is not None:
            return "%ddBm" % self.uniiTargetRSSI
        return "Unknown"
    

    opModeMap = ('Off', 'AP')
    def sysCurOpModeString(self):
        mode = self.sysCurOpMode()
        return mode is None and "Unknown" or self.opModeMap[int(mode)]

    def sysCurOpMode(self, default=None):
        return self.cacheRRDValue('sysCurOpMode', default)


InitializeClass(TrangoDevice)
