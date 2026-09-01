from tests.conftest import auth_header

async def test_list_atms_requires_auth(client, seeded_user):
    response = await client.get("/atms")
    assert response.status_code == 401

async def test_list_atms_any_authenticated_user(client, seeded_user):
    response = await client.get("/atms", headers=auth_header(seeded_user["auditor"]))
    assert response.status_code == 200

async def test_create_atm_forbidden_for_field_technician(client, seeded_user, seeded_branch):
    payload = {
        "serial_number": 123456,
        "model": "ATM Model X",
        "status": "Operational",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
    }
    response = await client.post("/atms", json=payload, headers=auth_header(seeded_user["technician"]))
    assert response.status_code == 403

async def test_create_atm_allowed_for_admin(client, seeded_user, seeded_branch):
    payload = {
        "serial_number": 123456,
        "model": "ATM Model X",
        "status": "Operational",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
    }
    response = await client.post("/atms", json=payload, headers=auth_header(seeded_user["admin"]))
    assert response.status_code == 201
    assert response.json()["serial_number"] == payload["serial_number"]


async def verify_cash_level(client, seeded_user, seeded_branch):
    admin_headers = auth_header(seeded_user["admin"])
    # Create an ATM first
    low_cash_atm = {
        "serial_number": 654321,
        "model": "ATM Model Y",
        "status": "Operational",
        "cash_level": 10,
        "branch_id": seeded_branch.id,
    }
    response = await client.post("/atms", json=low_cash_atm, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["cash_level"] == 10

    regular_atm = {
        "serial_number": 123456,
        "model": "ATM Model X",
        "status": "Operational",
        "cash_level": 80,
        "branch_id": seeded_branch.id,
    }
    response = await client.post("/atms", json=regular_atm, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["cash_level"] == 80
