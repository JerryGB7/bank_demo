

INSERT INTO branches(id, name, location_region, capacity) VALUES
    (1, 'Chase', 'LA', 50),
    (2, 'Wells Fargo', 'SG', 50),
    (3, 'America', 'COM', 50),
    (4, 'EastWest', 'ELM', 50);

INSERT INTO atms(id, serial_number, model, status, cash_level, branch_id) VALUES
    (11, 89454, 'chaseatm', 'Low-Cash', 19, 1 ),
    (12, 89455, 'chaseatm', 'Operational', 100, 1),
    (21, 22222, 'wellsatm', 'Operational', 50, 2),
    (22, 22223, 'wellsatm', 'Operational', 15, 2),
    (31, 3331, 'americaatm', 'Maintenance',1000, 3),
    (32, 3332, 'americaatm', 'Maintenance', 0, 3),
    (41, 4441, 'eastatm', 'Operational', 19, 4); 

INSERT INTO technicians(id, rbac) VALUES
    (10, 'Operation-Manager'),
    (11, 'Field-Technician'),
    (20, 'Operation-Manager'),
    (21, 'Field-Technician'),
    (30, 'Operation-Manager'),
    (31, 'Field-Technician'),
    (40, 'Operation-Manager'),
    (41, 'Field-Technician'),
    (999, 'Auditor');

-- INSERT INTO service_calls(id, title, priority, status, atm_id, technician_id) VALUES
--     (1, 'cash sensor not working','Critical', 'In-Progress', 31, 31),
--     (2, 'cash sensor not working','Critical', 'In-Progress', 32, 31);


SELECT setval('branches_id_seq', (SELECT MAX(id) FROM branches));
SELECT setval('atms_id_seq', (SELECT MAX(id) FROM atms));
SELECT setval('technicians_id_seq', (SELECT MAX(id) FROM technicians));
-- SELECT setval('service_calls_id_seq', (SELECT MAX(id) FROM service_calls));