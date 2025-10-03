#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.senec.senec.config import SenecInverterSetup
import logging

log = logging.getLogger(__name__)



class SenecInverter:
    def __init__(self, device_id: int, component_config: SenecInverterSetup) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SenecInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        

    def update(self, response) -> None:
     
        #PV Wechselrichter
        power=(round(response["ENERGY"]['GUI_INVERTER_POWER'],2)*-1)#convert to negative to supprt the model of OpenWB2

        _, exported = self.sim_counter.sim_count(power)
        
        inverter_state = InverterState(
            power=power,
            exported = exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SenecInverterSetup)
