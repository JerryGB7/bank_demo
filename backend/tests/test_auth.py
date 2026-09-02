from tests.conftest import auth_header

async def test_login(client, seeded_user):
    response = await client.post(
        "/auth/token",
        data={"username": "admin", "password": "adminpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_invalid_credentials(client):
    response = await client.post(
        "/auth/token",
        data={"username": "admin", "password": "wrongpass"}
    )
    assert response.status_code == 401

async def test_case_insensitive_login(client, seeded_user):
    response = await client.post(
        "/auth/token",
        data={"username": "ADMin", "password": "adminpass"}
    )
    assert response.status_code == 200

async def test_register_requires_admin(client, seeded_user):
    payload = {"username": "newuser", "password": "newpass", "role": "Field-Technician"}
    technician_response = await client.post(
        "/auth/register",
        json=payload,
        headers=auth_header(seeded_user["technician"])
    )
    assert technician_response.status_code == 403

    admin_response = await client.post(
        "/auth/register", json=payload, headers=auth_header(seeded_user["admin"])
    )
    assert admin_response.status_code == 201

