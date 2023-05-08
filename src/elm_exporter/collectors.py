import obd

from .car import Car
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import Collector

from typing import Iterable


class InfoCollector(Collector):
    """A collector for static text such as version information or VIN number"""

    def __init__(self, car: Car, commands: list[obd.OBDCommand]):
        self.car = car
        self.commands = commands

    def collect(self) -> Iterable[GaugeMetricFamily]:
        d = {}

        for command in self.commands:
            resp = self.car.query(command)
            v = resp.value

            if v is not None:
                if type(v) is bytearray:
                    d[command.name.lower()] = v.decode("ascii")
                else:
                    d[command.name.lower()] = str(v)

        yield InfoMetricFamily("car", "Static car information", value=d)
        self.car.reset_retries()


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

        self.car.reset_retries()
