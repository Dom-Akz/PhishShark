-- ============================================
-- Test Data for PhishingShark Application
-- USING QUOTES TO PRESERVE CASE SENSITIVITY
-- ============================================

-- 1. Create Departments
INSERT INTO "PhishingShark_departement" (id, name, chef_departement, description, created_at, updated_at) VALUES
(1, 'IT', 'John Smith', 'Information Technology', NOW(), NOW()),
(2, 'HR', 'Sarah Johnson', 'Human Resources', NOW(), NOW()),
(3, 'FIN', 'Mike Brown', 'Finance', NOW(), NOW()),
(4, 'MKT', 'Emma Wilson', 'Marketing', NOW(), NOW()),
(5, 'SAL', 'David Lee', 'Sales', NOW(), NOW()),
(6, 'OPS', 'Lisa Chen', 'Operations', NOW(), NOW());

-- 2. Create Administrators
INSERT INTO "PhishingShark_administrateur" (id, name, username, email, password, departement_id, is_active, is_supperuser, created_at, updated_at) VALUES
(1, 'Super Admin', 'superadmin', 'superadmin@phishinshark.com', 'pbkdf2_sha256$260000$...', NULL, true, true, NOW(), NOW()),
(2, 'John Smith', 'itadmin', 'john.smith@techcorp.com', 'pbkdf2_sha256$260000$...', 1, true, false, NOW(), NOW()),
(3, 'Sarah Johnson', 'hradmin', 'sarah.johnson@techcorp.com', 'pbkdf2_sha256$260000$...', 2, true, false, NOW(), NOW()),
(4, 'Mike Brown', 'financeadmin', 'mike.brown@techcorp.com', 'pbkdf2_sha256$260000$...', 3, true, false, NOW(), NOW());

-- 3. Create Companies
INSERT INTO "PhishingShark_entreprise" (id, name, alias, administrateur_id) VALUES
(1, 'TechCorp Solutions', 'TCS', 1),
(2, 'Global Finance Inc', 'GFI', 1),
(3, 'Digital Marketing Pro', 'DMP', 1);

-- 4. Create Employees
INSERT INTO "PhishingShark_employes" (id, matricule, ink, first_name, last_name, email, location, entreprise_id, departement_id, updated_at, created_at) VALUES
-- IT Department (dep_id = 1)
(1, 'TCS-Smith-JS-2026-001', 'IT_JohnSmith_NewYork_TCS', 'John', 'Smith', 'john.smith@techcorp.com', 'New York', 1, 1, NOW(), NOW()),
(2, 'TCS-Doe-JD-2026-002', 'IT_JohnSmith_Boston_TCS', 'Jane', 'Doe', 'jane.doe@techcorp.com', 'Boston', 1, 1, NOW(), NOW()),
(3, 'TCS-Johnson-BJ-2026-003', 'IT_JohnSmith_Chicago_TCS', 'Bob', 'Johnson', 'bob.johnson@techcorp.com', 'Chicago', 1, 1, NOW(), NOW()),
(4, 'TCS-Brown-AB-2026-004', 'IT_JohnSmith_Seattle_TCS', 'Alice', 'Brown', 'alice.brown@techcorp.com', 'Seattle', 1, 1, NOW(), NOW()),
(5, 'TCS-Wilson-CW-2026-005', 'IT_JohnSmith_Austin_TCS', 'Charlie', 'Wilson', 'charlie.wilson@techcorp.com', 'Austin', 1, 1, NOW(), NOW()),

-- HR Department (dep_id = 2)
(6, 'TCS-Johnson-SJ-2026-006', 'HR_SarahJohnson_NewYork_TCS', 'Sarah', 'Johnson', 'sarah.johnson@techcorp.com', 'New York', 1, 2, NOW(), NOW()),
(7, 'TCS-Williams-MW-2026-007', 'HR_SarahJohnson_Boston_TCS', 'Mike', 'Williams', 'mike.williams@techcorp.com', 'Boston', 1, 2, NOW(), NOW()),
(8, 'TCS-Davis-LD-2026-008', 'HR_SarahJohnson_Chicago_TCS', 'Lisa', 'Davis', 'lisa.davis@techcorp.com', 'Chicago', 1, 2, NOW(), NOW()),

-- Finance Department (dep_id = 3)
(9, 'TCS-Brown-MB-2026-009', 'FIN_MikeBrown_NewYork_TCS', 'Mike', 'Brown', 'mike.brown@techcorp.com', 'New York', 1, 3, NOW(), NOW()),
(10, 'TCS-Miller-SM-2026-010', 'FIN_MikeBrown_Boston_TCS', 'Susan', 'Miller', 'susan.miller@techcorp.com', 'Boston', 1, 3, NOW(), NOW()),
(11, 'TCS-Anderson-TA-2026-011', 'FIN_MikeBrown_Chicago_TCS', 'Tom', 'Anderson', 'tom.anderson@techcorp.com', 'Chicago', 1, 3, NOW(), NOW()),

-- Marketing Department (dep_id = 4)
(12, 'TCS-Wilson-EW-2026-012', 'MKT_EmmaWilson_NewYork_TCS', 'Emma', 'Wilson', 'emma.wilson@techcorp.com', 'New York', 1, 4, NOW(), NOW()),
(13, 'TCS-Taylor-CT-2026-013', 'MKT_EmmaWilson_Seattle_TCS', 'Chris', 'Taylor', 'chris.taylor@techcorp.com', 'Seattle', 1, 4, NOW(), NOW()),
(14, 'TCS-Martinez-AM-2026-014', 'MKT_EmmaWilson_Austin_TCS', 'Anna', 'Martinez', 'anna.martinez@techcorp.com', 'Austin', 1, 4, NOW(), NOW()),

-- Sales Department (dep_id = 5)
(15, 'TCS-Lee-DL-2026-015', 'SAL_DavidLee_NewYork_TCS', 'David', 'Lee', 'david.lee@techcorp.com', 'New York', 1, 5, NOW(), NOW()),
(16, 'TCS-Garcia-MG-2026-016', 'SAL_DavidLee_LosAngeles_TCS', 'Maria', 'Garcia', 'maria.garcia@techcorp.com', 'Los Angeles', 1, 5, NOW(), NOW()),
(17, 'TCS-Rodriguez-JR-2026-017', 'SAL_DavidLee_Miami_TCS', 'James', 'Rodriguez', 'james.rodriguez@techcorp.com', 'Miami', 1, 5, NOW(), NOW()),

-- Operations Department (dep_id = 6)
(18, 'TCS-Chen-LC-2026-018', 'OPS_LisaChen_NewYork_TCS', 'Lisa', 'Chen', 'lisa.chen@techcorp.com', 'New York', 1, 6, NOW(), NOW()),
(19, 'TCS-Nguyen-PN-2026-019', 'OPS_LisaChen_SanFrancisco_TCS', 'Peter', 'Nguyen', 'peter.nguyen@techcorp.com', 'San Francisco', 1, 6, NOW(), NOW()),
(20, 'TCS-Kim-RK-2026-020', 'OPS_LisaChen_Portland_TCS', 'Rachel', 'Kim', 'rachel.kim@techcorp.com', 'Portland', 1, 6, NOW(), NOW()),

-- Other companies
(21, 'GFI-White-JW-2026-001', 'FIN_JohnWhite_London_GFI', 'John', 'White', 'john.white@globalfinance.com', 'London', 2, 3, NOW(), NOW()),
(22, 'GFI-Black-MB-2026-002', 'FIN_MikeBlack_Paris_GFI', 'Mike', 'Black', 'mike.black@globalfinance.com', 'Paris', 2, 3, NOW(), NOW()),
(23, 'DMP-Green-LG-2026-001', 'MKT_LisaGreen_Berlin_DMP', 'Lisa', 'Green', 'lisa.green@digitalmarketing.com', 'Berlin', 3, 4, NOW(), NOW()),
(24, 'DMP-White-SW-2026-002', 'MKT_SteveWhite_Madrid_DMP', 'Steve', 'White', 'steve.white@digitalmarketing.com', 'Madrid', 3, 4, NOW(), NOW());

-- 5. Create Email Tracking Records
INSERT INTO "PhishingShark_emailtracking" (id, type, status, send_date, clicked_at, uuid, employe_id, ip_address) VALUES
(1, 'COMPANY_EMAIL', 'SENT', NOW() - INTERVAL '25 days', NULL, gen_random_uuid()::text, 1, NULL),
(2, 'PAYMENT_REQUEST', 'SENT', NOW() - INTERVAL '24 days', NULL, gen_random_uuid()::text, 2, NULL),
(3, 'JOB_OFFER', 'SENT', NOW() - INTERVAL '23 days', NULL, gen_random_uuid()::text, 3, NULL),
(4, 'ID_DEP', 'SENT', NOW() - INTERVAL '22 days', NULL, gen_random_uuid()::text, 4, NULL),
(5, 'SCAM_IPHONE', 'SENT', NOW() - INTERVAL '21 days', NULL, gen_random_uuid()::text, 5, NULL),
(6, 'SCAM_LOTTERY', 'CLICK', NOW() - INTERVAL '20 days', NOW() - INTERVAL '19 days', gen_random_uuid()::text, 6, '192.168.1.101'),
(7, 'SECURITY_ALERT', 'CLICK', NOW() - INTERVAL '19 days', NOW() - INTERVAL '18 days', gen_random_uuid()::text, 7, '192.168.1.102'),
(8, 'COMPANY_EMAIL', 'CLICK', NOW() - INTERVAL '18 days', NOW() - INTERVAL '17 days', gen_random_uuid()::text, 8, '192.168.1.103'),
(9, 'PAYMENT_REQUEST', 'CLICK', NOW() - INTERVAL '17 days', NOW() - INTERVAL '16 days', gen_random_uuid()::text, 9, '192.168.1.104'),
(10, 'JOB_OFFER', 'CLICK', NOW() - INTERVAL '16 days', NOW() - INTERVAL '15 days', gen_random_uuid()::text, 10, '192.168.1.105'),
(11, 'ID_DEP', 'CLICK', NOW() - INTERVAL '15 days', NOW() - INTERVAL '14 days', gen_random_uuid()::text, 11, '192.168.1.106'),
(12, 'SCAM_IPHONE', 'CLICK', NOW() - INTERVAL '14 days', NOW() - INTERVAL '13 days', gen_random_uuid()::text, 12, '192.168.1.107'),
(13, 'SCAM_LOTTERY', 'CLICK', NOW() - INTERVAL '13 days', NOW() - INTERVAL '12 days', gen_random_uuid()::text, 13, '192.168.1.108'),
(14, 'SECURITY_ALERT', 'CLICK', NOW() - INTERVAL '12 days', NOW() - INTERVAL '11 days', gen_random_uuid()::text, 14, '192.168.1.109'),
(15, 'COMPANY_EMAIL', 'RECEIVED', NOW() - INTERVAL '11 days', NULL, gen_random_uuid()::text, 15, NULL),
(16, 'PAYMENT_REQUEST', 'RECEIVED', NOW() - INTERVAL '10 days', NULL, gen_random_uuid()::text, 16, NULL),
(17, 'JOB_OFFER', 'RECEIVED', NOW() - INTERVAL '9 days', NULL, gen_random_uuid()::text, 17, NULL),
(18, 'ID_DEP', 'RECEIVED', NOW() - INTERVAL '8 days', NULL, gen_random_uuid()::text, 18, NULL),
(19, 'SCAM_IPHONE', 'RECEIVED', NOW() - INTERVAL '7 days', NULL, gen_random_uuid()::text, 19, NULL),
(20, 'SCAM_LOTTERY', 'SENT', NOW() - INTERVAL '6 days', NULL, gen_random_uuid()::text, 20, NULL),
(21, 'SECURITY_ALERT', 'CLICK', NOW() - INTERVAL '5 days', NOW() - INTERVAL '4 days', gen_random_uuid()::text, 21, '10.0.0.1'),
(22, 'COMPANY_EMAIL', 'SENT', NOW() - INTERVAL '4 days', NULL, gen_random_uuid()::text, 22, NULL),
(23, 'PAYMENT_REQUEST', 'CLICK', NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 days', gen_random_uuid()::text, 23, '10.0.0.2'),
(24, 'JOB_OFFER', 'SENT', NOW() - INTERVAL '2 days', NULL, gen_random_uuid()::text, 24, NULL),
(25, 'ID_DEP', 'CLICK', NOW() - INTERVAL '1 day', NOW(), gen_random_uuid()::text, 1, '10.0.0.3'),
(26, 'SCAM_IPHONE', 'SENT', NOW(), NULL, gen_random_uuid()::text, 2, NULL);

-- 6. Create QCM Results (Sensibilisation)
INSERT INTO "Sensibilisation_qcmresult" (id, employee_matricule, score, start_at, finish_at, totale_qcm_taken) VALUES
(1, 'TCS-Smith-JS-2026-001', 95, '09:00:00', '09:25:00', 2),
(2, 'TCS-Doe-JD-2026-002', 85, '10:00:00', '10:30:00', 1),
(3, 'TCS-Johnson-BJ-2026-003', 75, '11:00:00', '11:35:00', 3),
(4, 'TCS-Brown-AB-2026-004', 65, '13:00:00', '13:40:00', 1),
(5, 'TCS-Wilson-CW-2026-005', 55, '14:00:00', '14:45:00', 2),
(6, 'TCS-Johnson-SJ-2026-006', 90, '09:30:00', '09:55:00', 1),
(7, 'TCS-Williams-MW-2026-007', 80, '10:30:00', '11:05:00', 2),
(8, 'TCS-Davis-LD-2026-008', 70, '11:30:00', '12:10:00', 1),
(9, 'TCS-Brown-MB-2026-009', 88, '13:30:00', '14:00:00', 2),
(10, 'TCS-Miller-SM-2026-010', 78, '14:30:00', '15:10:00', 1),
(11, 'TCS-Anderson-TA-2026-011', 68, '15:00:00', '15:45:00', 3),
(12, 'TCS-Wilson-EW-2026-012', 92, '09:15:00', '09:40:00', 1),
(13, 'TCS-Taylor-CT-2026-013', 82, '10:15:00', '10:50:00', 2),
(14, 'TCS-Martinez-AM-2026-014', 72, '11:15:00', '11:55:00', 1),
(15, 'TCS-Lee-DL-2026-015', 60, '13:15:00', '14:00:00', 2),
(16, 'TCS-Garcia-MG-2026-016', 50, '14:15:00', '15:05:00', 1),
(17, 'TCS-Rodriguez-JR-2026-017', 45, '15:15:00', '16:00:00', 3),
(18, 'TCS-Chen-LC-2026-018', 98, '09:45:00', '10:05:00', 1),
(19, 'TCS-Nguyen-PN-2026-019', 87, '10:45:00', '11:15:00', 2),
(20, 'TCS-Kim-RK-2026-020', 77, '11:45:00', '12:25:00', 1),
(21, 'GFI-White-JW-2026-001', 91, '12:00:00', '12:30:00', 1),
(22, 'GFI-Black-MB-2026-002', 83, '13:00:00', '13:35:00', 2),
(23, 'DMP-Green-LG-2026-001', 89, '14:00:00', '14:28:00', 1),
(24, 'DMP-White-SW-2026-002', 76, '15:00:00', '15:40:00', 2);

-- 7. Create Sensibilisation Training Records
INSERT INTO "Sensibilisation_sensibilisation" (id, employee_matricule, totale_time) VALUES
(1, 'TCS-Smith-JS-2026-001', '01:30:00'),
(2, 'TCS-Doe-JD-2026-002', '01:15:00'),
(3, 'TCS-Johnson-BJ-2026-003', '00:45:00'),
(4, 'TCS-Brown-AB-2026-004', '01:00:00'),
(5, 'TCS-Wilson-CW-2026-005', '00:30:00'),
(6, 'TCS-Johnson-SJ-2026-006', '01:45:00'),
(7, 'TCS-Williams-MW-2026-007', '01:20:00'),
(8, 'TCS-Davis-LD-2026-008', '00:55:00'),
(9, 'TCS-Brown-MB-2026-009', '01:10:00'),
(10, 'TCS-Miller-SM-2026-010', '00:50:00'),
(11, 'TCS-Anderson-TA-2026-011', '01:25:00'),
(12, 'TCS-Wilson-EW-2026-012', '01:35:00'),
(13, 'TCS-Taylor-CT-2026-013', '00:40:00'),
(14, 'TCS-Martinez-AM-2026-014', '01:05:00'),
(15, 'TCS-Lee-DL-2026-015', '00:35:00'),
(16, 'TCS-Garcia-MG-2026-016', '00:25:00'),
(17, 'TCS-Rodriguez-JR-2026-017', '00:15:00'),
(18, 'TCS-Chen-LC-2026-018', '02:00:00'),
(19, 'TCS-Nguyen-PN-2026-019', '01:50:00'),
(20, 'TCS-Kim-RK-2026-020', '01:40:00'),
(21, 'GFI-White-JW-2026-001', '01:25:00'),
(22, 'GFI-Black-MB-2026-002', '01:10:00'),
(23, 'DMP-Green-LG-2026-001', '01:15:00'),
(24, 'DMP-White-SW-2026-002', '00:55:00');

-- ============================================
-- Verification Queries
-- ============================================

-- Check all tables have data
SELECT 'Departments' as table_name, COUNT(*) as count FROM "PhishingShark_departement"
UNION ALL
SELECT 'Administrators', COUNT(*) FROM "PhishingShark_administrateur"
UNION ALL
SELECT 'Companies', COUNT(*) FROM "PhishingShark_entreprise"
UNION ALL
SELECT 'Employees', COUNT(*) FROM "PhishingShark_employes"
UNION ALL
SELECT 'Email Tracking', COUNT(*) FROM "PhishingShark_emailtracking"
UNION ALL
SELECT 'QCM Results', COUNT(*) FROM "Sensibilisation_qcmresult"
UNION ALL
SELECT 'Training Records', COUNT(*) FROM "Sensibilisation_sensibilisation";
