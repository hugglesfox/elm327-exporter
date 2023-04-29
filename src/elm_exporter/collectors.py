import obd

from .car import Car
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import Collector

from typing import Iterable


class ObdCollector(Collector):
    """A collector for OBD commands.

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
            resp = self.car.query(command)
            v = resp.value

            if v is not None:
                yield GaugeMetricFamily(
                    command.name.lower(),
                    self._add_units(command.desc, v),
                    value=v.magnitude,
                )
            else:
                self.commands.remove(command)