#!/usr/bin/env python3
from typing import Any, Dict
import logging
from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.senec.senec.config import SenecCounterSetup

log = logging.getLogger(__name__)


class SenecCounter:
    def __init__(self, component_config: SenecCounterSetup, **kwargs: Any) -> None:
        self.component_config = dataclass_from_dict(SenecCounterSetup, component_config)
        self._kwargs: Dict[str, Any] = kwargs

    def initialize(self) -> None:
        self.__device_id: int = self._kwargs['device_id']
        self.__api = self._kwargs['api']
        log.info("SenecCounter initialize: device_id=%s component_id=%s", self.__device_id, self.component_config.id)
        self.store = get_counter_value_store(self.component_config.id)
        self.fault_state = FaultState(ComponentInfo.from_component_config(self.component_config))
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="counter")

    def update(self) -> None:
        log.debug("SenecCounter.update: fetching values from API")
        response = self.__api.get_values()

        currents = [round(response["PM1OBJ1"]['I_AC'][0], 2),
                    round(response["PM1OBJ1"]['I_AC'][1], 2),
                    round(response["PM1OBJ1"]['I_AC'][2], 2)]
        power = round(response["PM1OBJ1"]['P_TOTAL'], 2)
        frequency = round(response["PM1OBJ1"]['FREQ'], 2)
        powers = [round(response["PM1OBJ1"]['P_AC'][0], 2),
                  round(response["PM1OBJ1"]['P_AC'][1], 2),
                  round(response["PM1OBJ1"]['P_AC'][2], 2)]
        voltages = [round(response["PM1OBJ1"]['U_AC'][0], 2),
                    round(response["PM1OBJ1"]['U_AC'][1], 2),
                    round(response["PM1OBJ1"]['U_AC'][2], 2)]

        imported, exported = self.sim_counter.sim_count(power)
        log.debug("SenecCounter.update: power=%s freq=%s imported=%s exported=%s currents=%s voltages=%s powers=%s", power, frequency, imported, exported, currents, voltages, powers)

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
        log.debug("SenecCounter.update: state stored for component_id=%s", self.component_config.id)


component_descriptor = ComponentDescriptor(configuration_factory=SenecCounterSetup)
