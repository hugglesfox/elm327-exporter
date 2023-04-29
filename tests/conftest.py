import elm
import pytest

from starlette.testclient import TestClient

from elm_exporter import settings
from elm_exporter.app import app


@pytest.fixture(scope='session', autouse=True)
def emulator():
    print('hi')
    with elm.Elm() as emu:
        settings.ELM_PORT = emu.get_pty()
        yield emu


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
