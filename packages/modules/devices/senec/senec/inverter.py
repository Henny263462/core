#!/usr/bin/env python3
from typing import Any, Dict
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
    def __init__(self, component_config: SenecInverterSetup, **kwargs: Any) -> None:
        self.component_config = dataclass_from_dict(SenecInverterSetup, component_config)
        self._kwargs: Dict[str, Any] = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self._kwargs['device_id']
        self.__api = self._kwargs['api']
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        response = self.__api.get_values()
        # PV Wechselrichter
        power = (round(response["ENERGY"]['GUI_INVERTER_POWER'], 2) * -1)

        _, exported = self.sim_counter.sim_count(power)

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SenecInverterSetup)
