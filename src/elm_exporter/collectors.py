import obd

from .car import Car
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from prometheus_client.registry import Collector

from typing import Iterable


class InfoCollector(Collector):
    """A collector for static text such as version information or VIN number"""

    def __init__(self, car: Car, commands: list[str]):
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
            mode1_cmd = obd.commands[command]

            if (mode1 := self.car.query(mode1_cmd).value) is not None:
                g = GaugeMetricFamily(
                    command.lower(),
                    self._add_units(mode1_cmd.desc, mode1),
                    labels=["mode"],
                )

                g.add_metric(["1"], mode1.magnitude)

                mode2_cmd_name = "DTC_" + command

                if mode2_cmd_name in obd.commands:
                    mode2_cmd = obd.commands["DTC_" + command]

                    if (mode2 := self.car.query(mode2_cmd).value) is not None:
                        g.add_metric(["2"], mode2.magnitude)

                yield g

        self.car.reset_retries()
