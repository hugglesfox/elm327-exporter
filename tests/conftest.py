import elm
import pytest

from starlette.testclient import TestClient

from elm_exporter import settings
from elm_exporter.app import app

settings.LOG_LEVEL = "DEBUG"


@pytest.fixture(autouse=True)
def emulator():
    with elm.Elm() as emu:
        settings.ELM_PORT = emu.get_pty()
        yield emu


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
