#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, Union, List
import os
from modules.common import req

# from helpermodules.cli import run_using_positional_cli_args
# from modules.common import req
# from modules.common.abstract_device import DeviceDescriptor
# from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import (ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater,MultiComponentUpdater)

#from modules.devices.senec.senec import bat, counter, inverter, senec_device 
from modules.devices.senec.senec.bat import SenecBat
from modules.devices.senec.senec.config import Senec, SenecConfiguration, SenecBatConfiguration, SenecBatSetup, SenecCounterSetup, SenecInverterSetup
from modules.devices.senec.senec.counter import SenecCounter
from modules.devices.senec.senec.inverter import SenecInverter
from modules.devices.senec.senec.senec_device import Senec_Connection

log = logging.getLogger(__name__)


#def create_device(device_config: Senec):
def create_device(device_config: Senec) -> ConfigurableDevice:
    def create_bat_component(component_config: SenecBatSetup) -> SenecBat:
        return SenecBat(device_config.id, component_config)
        #return SenecBat(device_config.id, component_config, device_config.configuration.ip_address,
        #                     get_device_generation(device_config.configuration.ip_address))

    

    def create_counter_component(component_config: SenecCounterSetup)-> SenecCounter:
        return SenecCounter(device_config.id, component_config)
        #return SenecCounter(device_config.id, component_config, device_config.configuration.ip_address,
         #                    get_device_generation(device_config.configuration.ip_address))

    def create_inverter_component(component_config: SenecInverterSetup) -> SenecInverter:
        return SenecInverter(device_config.id, component_config)
        #return SenecInverter(device_config.id, component_config, device_config.configuration.ip_address,
         #                    get_device_generation(device_config.configuration.ip_address))

    def update_components(components: Iterable[Union[SenecBat, SenecCounter, SenecInverter]]):
        
        #init api
        api = Senec_Connection(device_config.configuration.ip_address)
        response=api.get_values()
        
        log.debug("Geraeteinformationen")
        #log.debug("Aktueller Status    : {0}".format(response["STATISTIC"]['CURRENT_STATE']))
        #log.debug("Kapazitaet          : {0}".format(response["FACTORY"]['DESIGN_CAPACITY']))
        log.debug("Batterie - Laden/Entladen    : {0} W".format(round(response["ENERGY"]['GUI_BAT_DATA_POWER'],2)))
        log.debug("Power - Einspeisung / Bezug  : {0} W".format(round(response["ENERGY"]['GUI_GRID_POW'],2)))
        log.debug("Power - Hausverbrauch        : {0} W".format(round(response["ENERGY"]['GUI_HOUSE_POW'],2)))
        
        log.debug("")
        log.debug("PV Leistung - String 1       : {0} W".format(round(response["PV1"]['MPP_POWER'][0],2)))
        log.debug("PV Leistung - String 2       : {0} W".format(round(response["PV1"]['MPP_POWER'][1],2)))
        log.debug("PV Leistung - String 3       : {0} W".format(round(response["PV1"]['MPP_POWER'][2],2)))
        log.debug("PV Export Ratio              : {0} %".format(round(response["PV1"]['POWER_RATIO'],2)))
        log.debug("PV Export P_TOTAL              : {0} %".format(round(response["PV1"]['P_TOTAL'],2)))
        
        
        log.debug("Frequency                    : {0} Hz".format(round(response["PM1OBJ1"]['FREQ'],2)))
        log.debug("Spannung (1)                 : {0} V".format(round(response["PM1OBJ1"]['U_AC'][0],2)))
        log.debug("Spannung (2)                 : {0} V".format(round(response["PM1OBJ1"]['U_AC'][1],2)))
        log.debug("Spannung (3)                 : {0} V".format(round(response["PM1OBJ1"]['U_AC'][2],2)))
        log.debug("Strom (1)                    : {0} A".format(round(response["PM1OBJ1"]['I_AC'][0],2)))
        log.debug("Strom (2)                    : {0} A".format(round(response["PM1OBJ1"]['I_AC'][1],2)))
        log.debug("Strom (3)                    : {0} A".format(round(response["PM1OBJ1"]['I_AC'][2],2)))
        log.debug("Leistung (1)                 : {0} W".format(round(response["PM1OBJ1"]['P_AC'][0],2)))
        log.debug("Leistung (2)                 : {0} W".format(round(response["PM1OBJ1"]['P_AC'][1],2)))
        log.debug("Leistung (3)                 : {0} W".format(round(response["PM1OBJ1"]['P_AC'][2],2)))
        log.debug("Gesamtleistung               : {0} W".format(round(response["PM1OBJ1"]['P_TOTAL'],2)))
        
        log.debug("Batterie - Laden/Entladen    : {0} W".format(round(response["ENERGY"]['GUI_BAT_DATA_POWER'],2)))
        log.debug("Batterie - Fuellstand        : {0} %".format(round(response["ENERGY"]['GUI_BAT_DATA_FUEL_CHARGE'],2)))
        log.debug("Power - PV Leistung          : {0} W".format(round(response["ENERGY"]['GUI_INVERTER_POWER'],2)))
        
        #log.debug("Gesamtlademenge              : {0} Wh".format(round(response["STATISTIC"]['LIVE_BAT_CHARGE'],2)))
        #log.debug("Gesamtentlademenge           : {0} Wh".format(round(response["STATISTIC"]['LIVE_BAT_DISCHARGE'],2)))
        #log.debug("Gesamtimport                 : {0} Wh".format(round(response["STATISTIC"]['LIVE_GRID_IMPORT'],2)))
        #log.debug("Gesamteinspeisung            : {0} Wh".format(round(response["STATISTIC"]['LIVE_GRID_EXPORT'],2)))
        #log.debug("Gesamt PV Erzeugung (vom WR) : {0} Wh".format(round(response["STATISTIC"]['LIVE_PV_GEN'],2)))
                
        for component in components:
            component.update(response)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
        #component_updater=IndependentComponentUpdater(lambda component: component.update())
    )


# COMPONENT_TYPE_TO_MODULE = {
#    "bat": bat,
 #   "counter": counter,
#    "inverter": inverter
#}
device_descriptor = DeviceDescriptor(configuration_factory=Senec)
