SELECT
    b.id AS branch_id,
    b.name,
    atm.id AS atm_id
FROM atms atm
JOIN branches b ON b.id = atm.branch_id
ORDER BY b.id;
