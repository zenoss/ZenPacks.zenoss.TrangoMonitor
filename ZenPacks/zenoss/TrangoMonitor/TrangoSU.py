##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""TrangoSU

TrangoSU represents a subscriber unit from TRANGOM5800S-MIB.

$Id: $"""

__version__ = "$Revision: $"[11:-2]

import locale

from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


class TrangoSU(DeviceComponent, ManagedEntity):
    """TrangoSU object"""

    portal_type = meta_type = 'TrangoSU'
    
    mac = ""
    polling = ""
    peerGroup = ""
    cir = None
    mir = None
    ipAddr = ""
    remarks = ""
    hwVer = ""
    fwVer = ""
    fpgaVer = ""
    checksum = ""
    association = None
    distance = None

    _properties = (
        {'id':'mac', 'type':'string', 'mode':'w'},
        {'id':'polling', 'type':'string', 'mode':'w'},
        {'id':'peerGroup', 'type':'string', 'mode':'w'},
        {'id':'cir', 'type':'int', 'mode':'w'},
        {'id':'mir', 'type':'int', 'mode':'w'},
        {'id':'ipAddr', 'type':'string', 'mode':'w'},
        {'id':'remarks', 'type':'string', 'mode':'w'},
        {'id':'hwVer', 'type':'string', 'mode':'w'},
        {'id':'fwVer', 'type':'string', 'mode':'w'},
        {'id':'fpgaVer', 'type':'string', 'mode':'w'},
        {'id':'checksum', 'type':'string', 'mode':'w'},
        {'id':'association', 'type':'boolean', 'mode':'w'},
        {'id':'distance', 'type':'int', 'mode':'w'},
        )

    _relations = (
        ("accessPoint", ToOne(ToManyCont,
            "ZenPacks.zenoss.TrangoMonitor.TrangoDevice", "subscriberUnits")),
        )
    
    factory_type_information = ( 
        { 
            'id'             : 'TrangoSU',
            'meta_type'      : 'TrangoSU',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'TrangoSU_icon.gif',
            'product'        : 'TrangoMonitor',
            'immediate_view' : 'viewTrangoSU',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewTrangoSU'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS,)
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW,)
                },
            )
          },
        )
        
    def manage_editTrangoSU(self, monitor=False, REQUEST=None):
        """
        Edit this TrangoSU from the web.
        """
        self.monitor = monitor
        self.index_object()
        
        if REQUEST:
            REQUEST['message'] = "SU updated"
            return self.callZenScreen(REQUEST)


    def viewName(self): return "SU" + self.id
    name = viewName
    
    def primarySortKey(self):
        return int(self.id)


    def device(self):
        return self.accessPoint()
    
    
    def monitored(self):
        if not self.association:
            return False
        elif not self.ipAddr or self.ipAddr == "0.0.0.0":
            return False
        return self.monitor
    
    
    def rssiFromSU(self, default=None):
        return self.cacheRRDValue('rssiFromSU', default)
    
    def rssiFromSUString(self):
        rssi = self.rssiFromSU()
        return rssi is None and "Unknown" or "%ddBm" % rssi
    
    
    def rssiFromAP(self, default=None):
        return self.cacheRRDValue('rssiFromAP', default)
    
    def rssiFromAPString(self):
        rssi = self.rssiFromAP()
        return rssi is None and "Unknown" or "%ddBm" % rssi
    
    def rssiString(self):
        fromAP = str(self.rssiFromAP(default="Unknown"))
        fromSU = str(self.rssiFromSU(default="Unknown"))
        return "%s / %s" % (fromAP, fromSU)
    
    
    def txPower(self, default=None):
        return self.cacheRRDValue('txPower', default)
    
    def txPowerString(self):
        power = self.txPower()
        return power is None and "Unknown" or "%ddBm" % power
        

    def getRRDNames(self):
        return [
            'rssiFromSU_rssiFromSU',
            'rssiFromAP_rssiFromAP',
            'txPower_txPower',
            'rfInOctets_rfInOctets',
            'rfOutOctets_rfOutOctets',
            'temperature_temperature',
            ]


InitializeClass(TrangoSU)
