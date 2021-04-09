import pytest
from server import app as scheduler_app

@pytest.fixture
def app():
    yield scheduler_app


@pytest.fixture
def client(app):
    return app.test_client()
