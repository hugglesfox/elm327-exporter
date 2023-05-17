import obd

from .car import Car
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import Collector

from typing import Iterable


class ObdCollector(Collector):
    """A collector for mode 1 and 2 OBD commands.

    Generates prometheus Guages for each of the given OBD commands.
    """

    def __init__(self, car: Car, commands: list[obd.OBDCommand]):
        self.car = car
        self.commands = commands

    def _add_units(self, desc: str, value: obd.Unit.Quantity) -> str:
        units = value.units

        if units is not None:
            return "{} ({:~P})".format(desc, units)

        return desc

    def collect(self) -> Iterable[GaugeMetricFamily]:
        for command in self.commands:
            c = obd.commands[command]

            if (v := self.car.query(c).value) is not None:
                yield GaugeMetricFamily(
                    command.lower(), self._add_units(c.desc, v), value=v.magnitude
                )

        self.car.reset_retries()
