from os import remove

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    client = TestClient(app)
    yield client
    client.close()

    try:
        remove("./sqlite.db")
    except FileNotFoundError:
        try:
            remove("./app./test/sqlite.db")
        except FileNotFoundError:
            print("File DB Not Found")
