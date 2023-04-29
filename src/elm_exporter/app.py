import contextlib

from . import settings, car
from prometheus_client import make_asgi_app
from starlette.applications import Starlette
from starlette.routing import Mount


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    yield
    car.close()


app = Starlette(
    debug=settings.DEBUG or settings.LOG_LEVEL == "DEBUG",
    lifespan=lifespan,
    routes=[Mount("/metrics", make_asgi_app())],
)
