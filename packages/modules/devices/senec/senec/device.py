#!/usr/bin/env python3
import logging
from typing import Iterable, Union

from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.devices.senec.senec.bat import SenecBat
from modules.devices.senec.senec.config import (
    Senec,
    SenecBatSetup,
    SenecCounterSetup,
    SenecInverterSetup,
)
from modules.devices.senec.senec.counter import SenecCounter
from modules.devices.senec.senec.inverter import SenecInverter
from modules.devices.senec.senec.senec_device import Senec_Connection

log = logging.getLogger(__name__)


#def create_device(device_config: Senec):
def create_device(device_config: Senec) -> ConfigurableDevice:
    api = None

    def create_bat_component(component_config: SenecBatSetup) -> SenecBat:
        return SenecBat(component_config, device_id=device_config.id, api=api)
        #return SenecBat(device_config.id, component_config, device_config.configuration.ip_address,
        #                     get_device_generation(device_config.configuration.ip_address))

    

    def create_counter_component(component_config: SenecCounterSetup)-> SenecCounter:
        return SenecCounter(component_config, device_id=device_config.id, api=api)
        #return SenecCounter(device_config.id, component_config, device_config.configuration.ip_address,
         #                    get_device_generation(device_config.configuration.ip_address))

    def create_inverter_component(component_config: SenecInverterSetup) -> SenecInverter:
        return SenecInverter(component_config, device_id=device_config.id, api=api)
        #return SenecInverter(device_config.id, component_config, device_config.configuration.ip_address,
         #                    get_device_generation(device_config.configuration.ip_address))

    def update_components(components: Iterable[Union[SenecBat, SenecCounter, SenecInverter]]):
        log.debug("Senec.update_components: updating %s components", len(list(components)))
        for component in components:
            with SingleComponentUpdateContext(component.fault_state):
                component.update()

    def initializer():
        nonlocal api
        log.info("Senec.initializer: creating API client for ip=%s", device_config.configuration.ip_address)
        api = Senec_Connection(device_config.configuration.ip_address)

    return ConfigurableDevice(
        device_config=device_config,
        initializer=initializer,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components),
    )


# COMPONENT_TYPE_TO_MODULE = {
#    "bat": bat,
 #   "counter": counter,
#    "inverter": inverter
#}
device_descriptor = DeviceDescriptor(configuration_factory=Senec)
