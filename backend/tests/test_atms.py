from tests.conftest import auth_header
from app.models import ATM, Branch, ServiceCall, Service_Call_Priority, Service_Call_Status, Technician

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

async def test_delete_atm_forbidden_for_field_technician(client, seeded_user, seeded_branch):
    payload = {
        "serial_number": 123456,
        "model": "ATM Model X",
        "status": "Operational",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
    }
    created = await client.post("/atms", json=payload, headers=auth_header(seeded_user["admin"]))

    response = await client.delete(
        f"/atms/{created.json()['id']}",
        headers=auth_header(seeded_user["technician"]),
    )

    assert response.status_code == 403

async def test_delete_atm_allowed_for_admin(client, seeded_user, seeded_branch):
    payload = {
        "serial_number": 123456,
        "model": "ATM Model X",
        "status": "Operational",
        "cash_level": 50,
        "branch_id": seeded_branch.id,
    }
    created = await client.post("/atms", json=payload, headers=auth_header(seeded_user["admin"]))
    atm_id = created.json()["id"]

    response = await client.delete(f"/atms/{atm_id}", headers=auth_header(seeded_user["admin"]))

    assert response.status_code == 204
    assert (await client.get(f"/atms/atm_id?atm_id={atm_id}", headers=auth_header(seeded_user["admin"]))).status_code == 404

async def test_delete_atm_returns_not_found(client, seeded_user):
    response = await client.delete("/atms/999999", headers=auth_header(seeded_user["admin"]))

    assert response.status_code == 404


async def test_reporting_lines_counts_distinct_technicians_with_active_calls(
    client, db_session, seeded_user, seeded_branch
):
    second_branch = Branch(
        name="Other Branch", location_region="Other Location", capacity=100, supervisor_id=2
    )
    technicians = [
        Technician(name="Tech One", branch=seeded_branch),
        Technician(name="Tech Two", branch=seeded_branch),
        Technician(name="Other Tech", branch=second_branch),
    ]
    atms = [
        ATM(serial_number=100001, model="Model A", cash_level=80, branch=seeded_branch),
        ATM(serial_number=100002, model="Model A", cash_level=80, branch=seeded_branch),
        ATM(serial_number=100003, model="Model A", cash_level=80, branch=second_branch),
    ]
    db_session.add_all([second_branch, *technicians, *atms])
    await db_session.flush()
    db_session.add_all([
        ServiceCall(
            title="Refill one", priority=Service_Call_Priority.LOW,
            status=Service_Call_Status.PENDING, atm=atms[0], technician=technicians[0],
        ),
        ServiceCall(
            title="Repair one", priority=Service_Call_Priority.MEDIUM,
            status=Service_Call_Status.IN_PROGRESS, atm=atms[1], technician=technicians[0],
        ),
        ServiceCall(
            title="Repair two", priority=Service_Call_Priority.CRITICAL,
            status=Service_Call_Status.COMPLETED, atm=atms[1], technician=technicians[1],
        ),
        ServiceCall(
            title="Other branch call", priority=Service_Call_Priority.LOW,
            status=Service_Call_Status.PENDING, atm=atms[2], technician=technicians[2],
        ),
    ])
    await db_session.commit()

    response = await client.get(
        f"/service_calls/reporting_lines?supervisor_id={seeded_branch.supervisor_id}",
        headers=auth_header(seeded_user["auditor"]),
    )

    assert response.status_code == 200
    assert response.json() == {
        "supervisor_id": seeded_branch.supervisor_id,
        "technicians_with_active_calls": 1,
    }


async def test_reporting_lines_requires_auth(client, seeded_branch):
    response = await client.get(
        f"/service_calls/reporting_lines?supervisor_id={seeded_branch.supervisor_id}"
    )

    assert response.status_code == 401


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
