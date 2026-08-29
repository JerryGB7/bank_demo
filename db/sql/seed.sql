

INSERT INTO branches(id, name, location_region, capacity, supervisor_id) VALUES
    (1, 'Chase', 'LA', 50, 10),
    (2, 'Wells Fargo', 'SG', 50, 20),
    (3, 'America', 'COM', 50, 30),
    (4, 'EastWest', 'ELM', 50, 40);

INSERT INTO technicians(id, name, branch_id) VALUES
    (10, 'Susan',1),
    (11, 'Leon',1),
    (20, 'Barry',2),
    (21, 'Chloe',2),
    (30, 'Serine',3),
    (31, 'Grace',3),
    (40, 'Billy',4),
    (41, 'James',4),
    (90, 'Cyntia',1);    

INSERT INTO atms(id, serial_number, model, status, cash_level, branch_id, technician_id) VALUES
    (11, 89454, 'chaseatm', 'Low-Cash', 19, 1, 11),
    (12, 89455, 'chaseatm', 'Operational', 100, 1, 21),
    (21, 22222, 'wellsatm', 'Operational', 50, 2, 21),
    (22, 22223, 'wellsatm', 'Operational', 15, 2, 21),
    (31, 3331, 'americaatm', 'Maintenance',100, 3, 31),
    (32, 3332, 'americaatm', 'Offline', 0, 3, 31),
    (41, 4441, 'eastatm', 'Operational', 19, 4, 41); 


INSERT INTO service_calls(id, title, priority, status, atm_id, technician_id) VALUES
     (1, 'cash sensor not working','Critical', 'In-Progress', 31, 31),
     (2, 'cash sensor not working','Critical', 'In-Progress', 32, 31);

INSERT INTO diagnostic_reports(id, service_call_id, file_url, notes) VALUES
     (1, 1, 'demo.url', 'In-Progress'),
     (2, 2, 'demo.url', 'In-Progress');


SELECT setval('branches_id_seq', (SELECT MAX(id) FROM branches));
SELECT setval('technicians_id_seq', (SELECT MAX(id) FROM technicians));
SELECT setval('atms_id_seq', (SELECT MAX(id) FROM atms));
SELECT setval('service_calls_id_seq', (SELECT MAX(id) FROM service_calls));