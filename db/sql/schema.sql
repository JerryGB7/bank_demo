CREATE TYPE atm_status as ENUM ('Operational', 'Low-Cash', 'Maintenance', 'Offline');
CREATE TYPE service_call_priority as ENUM ('Low', 'Medium', 'Critical');
CREATE TYPE service_call_status as ENUM ('Pending', 'In-Progress', 'Completed', 'Failed');
CREATE TYPE technician_rbac as ENUM ('Operation-Manager', 'Field-Technician', 'Auditor');

CREATE TABLE branches(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_region VARCHAR(5) NOT NULL,
    capacity INTEGER NOT NULL,
    supervisor_id INTEGER NOT NULL
);

CREATE TABLE technicians(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    branch_id INTEGER NOT NULL REFERENCES branches(id)
);


CREATE TABLE atms(
    id SERIAL PRIMARY KEY,
    serial_number INTEGER NOT NULL UNIQUE,
    model VARCHAR(50) NOT NULL,
    status atm_status NOT NULL DEFAULT 'Operational',
    cash_level INTEGER NOT NULL,
    branch_id INTEGER NOT NULL REFERENCES branches(id),
    technician_id INTEGER NOT NULL REFERENCES technicians(id)
);


CREATE TABLE service_calls(
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    priority service_call_priority NOT NULL,
    status service_call_status NOT NULL,
    atm_id INTEGER NOT NULL REFERENCES atms(id),
    technician_id INTEGER NOT NULL REFERENCES technicians(id)
);

CREATE TABLE diagnostic_reports(
    id SERIAL PRIMARY KEY,
    service_call_id INTEGER NOT NULL REFERENCES service_calls(id)
    file_url TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);