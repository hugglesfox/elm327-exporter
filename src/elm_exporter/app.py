import contextlib
import obd

from . import COMMANDS, settings
from .car import Car
from .collectors import ObdCollector

from prometheus_client import make_asgi_app
from prometheus_client.core import REGISTRY

from starlette.applications import Starlette
from starlette.routing import Mount


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    car = Car()

    commands = [obd.commands[cmd] for cmd in COMMANDS]
    REGISTRY.register(ObdCollector(car, commands))

    yield

    car.close()


app = Starlette(
    debug=settings.DEBUG or settings.LOG_LEVEL == "DEBUG",
    lifespan=lifespan,
    routes=[Mount("/metrics", make_asgi_app())],
)
