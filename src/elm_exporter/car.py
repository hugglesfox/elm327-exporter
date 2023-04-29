import obd
import time

from . import settings

obd.logger.setLevel(settings.LOG_LEVEL)


class Car:
    """A wrapper around the obd.OBD class.

    The wrapper provides the ability to reconnect to the ELM if the ELM or car
    becomes disconnected. The number of reconnection attempts are defined using
    the `ELM_MAX_RETRIES` setting.
    """

    def __init__(self):
        self._car = obd.OBD(settings.ELM_PORT)
        self._retries = 0

    def query(self, command: obd.OBDCommand) -> obd.OBDResponse:
        """See obd.OBD.query() documentation"""
        connected = self._car.status() != obd.utils.OBDStatus.CAR_CONNECTED
        while connected and self._retries <= settings.ELM_MAX_RETRIES:
            self._car.close()
            self._car = obd.OBD(settings.ELM_PORT)
            time.sleep(self._retries)
            self._retries += 1

        self._retries = 0
        return self._car.query(command)

    def close(self):
        """See obd.OBD.close() documentation"""
        self._car.close()
