# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from fa_passkeys.config import settings
from fa_passkeys.models import User

client = TestClient(app)


@pytest.fixture(autouse=True)
async def setup_and_teardown():
    # Setup before tests
    await User.get_motor_collection().drop()
    yield
    # Teardown after tests
    await User.get_motor_collection().drop()


def test_register_and_authenticate():
    username = "testuser"

    # Registration options
    response = client.post("/auth/register/options", json={"username": username})
    assert response.status_code == 200
    # Note: In actual tests, you would need to simulate client-side WebAuthn interactions

    # Registration complete
    # Simulate client data for registration complete
    # Skipping actual data for brevity
    response = client.post("/auth/register/complete", data=b"client data")
    assert response.status_code == 200

    # Authentication options
    response = client.post("/auth/authenticate/options", json={"username": username})
    assert response.status_code == 200

    # Authentication complete
    # Simulate client data for authentication complete
    response = client.post("/auth/authenticate/complete", data=b"client data")
    assert response.status_code == 200
    assert "access_token" in response.json()
