import pytest
from fastapi.testclient import TestClient

from small_ecommerce.main import app


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client
