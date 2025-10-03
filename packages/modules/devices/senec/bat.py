#!/usr/bin/env python3
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.senec.senec.config import SenecBatSetup

class SenecBat:
    def init(self, device_id: int, component_config: SenecBatSetup) -> None:
        self.device_id = device_id
        self.component_config = dataclass_from_dict(SenecBatSetup, component_config)
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.sim_counter = SimCounter(self.device_id, self.component_config.id, prefix="speicher")

    def update(self, response) -> None:

        power=round(response["ENERGY"]['GUI_BAT_DATA_POWER'],2)
        soc=round(response["ENERGY"]['GUI_BAT_DATA_FUEL_CHARGE'],2)
        #imported=(round(response["STATISTIC"]['LIVE_BAT_CHARGE']1000,3)),
        #exported=(round(response["STATISTIC"]['LIVE_BAT_DISCHARGE']1000,3))
        imported, exported = self.sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

component_descriptor = ComponentDescriptor(configuration_factory=SenecBatSetup)