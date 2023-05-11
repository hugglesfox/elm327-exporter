import contextlib
import obd

from . import COMMANDS, settings
from .car import Car
from .collectors import ObdCollector, InfoCollector

from prometheus_client import make_asgi_app
from prometheus_client.core import REGISTRY

from starlette.applications import Starlette
from starlette.routing import Mount


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    car = Car()

    obd_collector = ObdCollector(car, COMMANDS)
    REGISTRY.register(obd_collector)

    info_collector = InfoCollector(
        car, [obd.commands.ELM_VERSION, obd.commands.VIN, obd.commands.FUEL_TYPE]
    )
    REGISTRY.register(info_collector)

    yield

    REGISTRY.unregister(obd_collector)
    REGISTRY.unregister(info_collector)

    if settings.ELM_AUTO_LP:
        car.dev.low_power()

    car.close()


app = Starlette(
    debug=settings.DEBUG or settings.LOG_LEVEL == "DEBUG",
    lifespan=lifespan,
    routes=[Mount("/metrics", make_asgi_app())],
)
