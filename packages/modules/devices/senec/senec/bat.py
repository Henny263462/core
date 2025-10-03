#!/usr/bin/env python3
from typing import Any, Dict
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.senec.senec.config import SenecBatSetup


class SenecBat:
    def __init__(self, component_config: SenecBatSetup, **kwargs: Any) -> None:
        self.component_config = dataclass_from_dict(SenecBatSetup, component_config)
        self._kwargs: Dict[str, Any] = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self._kwargs['device_id']
        self.__api = self._kwargs['api']
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        response = self.__api.get_values()

        power = round(response["ENERGY"]['GUI_BAT_DATA_POWER'], 2)
        soc = round(response["ENERGY"]['GUI_BAT_DATA_FUEL_CHARGE'], 2)
        imported, exported = self.sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)

component_descriptor = ComponentDescriptor(configuration_factory=SenecBatSetup)