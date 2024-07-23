import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    # Arrange (organização)
    return TestClient(app)
