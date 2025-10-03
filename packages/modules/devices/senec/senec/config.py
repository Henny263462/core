from typing import Optional
from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup
from ..vendor import vendor_descriptor


@auto_str
#class SenecConfiguration:
#    def __init__(self, ip_address: Optional[str] = None):
#        self.ip_address = ip_address
        
class SenecConfiguration:
    def __init__(self, ip_address: Optional[str] = "192.168.0.21"):
        self.ip_address = ip_address
        


@auto_str
class Senec:
    def __init__(self,
                 name: str = "Senec",
                 type: str = "senec",
                 id: int = 0,
                 configuration: SenecConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.vendor = vendor_descriptor.configuration_factory().type
        self.id = id
        self.configuration = configuration or SenecConfiguration()


@auto_str
class SenecBatConfiguration:
    def __init__(self):
        pass
     


@auto_str
class SenecBatSetup(ComponentSetup[SenecBatConfiguration]):
    def __init__(self,
                 name: str = "Senec Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SenecBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SenecBatConfiguration())


@auto_str
class SenecCounterConfiguration:
    def __init__(self):
        pass


@auto_str
class SenecCounterSetup(ComponentSetup[SenecCounterConfiguration]):
    def __init__(self,
                 name: str = "Senec EVU Zähler angebunden über den Speicher",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SenecCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SenecCounterConfiguration())


@auto_str
class SenecInverterConfiguration:
    def __init__(self):
        pass


@auto_str
class SenecInverterSetup(ComponentSetup[SenecInverterConfiguration]):
    def __init__(self,
                 name: str = "Senec Wechselrichter Daten ausgelesen über den Speicher",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SenecInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SenecInverterConfiguration())
