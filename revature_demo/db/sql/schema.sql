CREATE TYPE atm_status as ENUM ('Operational', 'Low-Cash', 'Maintenance', 'Offline');
CREATE TYPE service_call_priority as ENUM ('Low', 'Medium', 'Critical');
CREATE TYPE service_call_status as ENUM ('Pending', 'In-Progress', 'Completed', 'Failed');
CREATE TYPE technician_rbac as ENUM ('Operation-Manager', 'Field-Technician', 'Auditor');

CREATE TABLE branches(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_region VARCHAR(5) NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE atms(
    id SERIAL PRIMARY KEY,
    serial_number INTEGER NOT NULL UNIQUE,
    model VARCHAR(50) NOT NULL,
    status atm_status NOT NULL DEFAULT 'Operational',
    cash_level NUMERIC(5,2) NOT NULL CHECK(cash_level BETWEEN 0 AND 100),
    branch_id INTEGER NOT NULL REFERENCES branches(id)
);

CREATE TABLE technicians(
    id SERIAL PRIMARY KEY,
    rbac technician_rbac NOT NULL
);

CREATE TABLE service_calls(
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    priority service_call_priority NOT NULL,
    status service_call_status NOT NULL,
    atm_id INTEGER NOT NULL REFERENCES atms(id),
    technician_id INTEGER NOT NULL REFERENCES technicians(id)
);

-- CREATE TABLE diagnostic_logs(
--     id SERIAL PRIMARY KEY,
--     file_url TEXT NOT NULL,
--     notes TEXT,
--     timestamp TIMESTAMP NOT NULL DEFAULT NOW()
-- );