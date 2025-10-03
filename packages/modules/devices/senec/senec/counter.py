#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.senec.senec.config import SenecCounterSetup


class SenecCounter:
    def __init__(self, device_id: int, component_config: SenecCounterSetup) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SenecCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="counter")

    def update(self, response):

        currents=[round(response["PM1OBJ1"]['I_AC'][0],2),round(response["PM1OBJ1"]['I_AC'][1],2),round(response["PM1OBJ1"]['I_AC'][2],2)]
        #imported=round(response["STATISTIC"]['LIVE_GRID_IMPORT']*1000,2)
        #exported=round(response["STATISTIC"]['LIVE_GRID_EXPORT']*1000,2)
        #Hausverbrauch! 
        #power=round(response["ENERGY"]['GUI_HOUSE_POW'],2)
        power=round(response["PM1OBJ1"]['P_TOTAL'],2)
        #frequency=round(response["ENERGY"]['GUI_HOUSE_POW'],2)
        frequency=round(response["PM1OBJ1"]['FREQ'],2)
        
        #power_factors=power_factors
        powers=[round(response["PM1OBJ1"]['P_AC'][0],2),round(response["PM1OBJ1"]['P_AC'][1],2),round(response["PM1OBJ1"]['P_AC'][2],2)]
        voltages=[round(response["PM1OBJ1"]['U_AC'][0],2),round(response["PM1OBJ1"]['U_AC'][1],2),round(response["PM1OBJ1"]['U_AC'][2],2)]

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            currents=currents, 
            imported=imported, 
            exported=exported,
            power=power,
            frequency=frequency,
            powers=powers,
            voltages=voltages
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SenecCounterSetup)
