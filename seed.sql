-- ============================================
-- Geo Bucket System - Sample Data Seed Script
-- ============================================

-- Enable PostGIS extensions if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Clear existing data (optional - uncomment for fresh seed)
-- DELETE FROM properties_property;
-- DELETE FROM geo_geobucket;

-- ============================================
-- 1. GEO BUCKETS - Popular Lagos Areas
-- ============================================

INSERT INTO geo_geobucket (id, name, normalized_name, center, radius_meters, created_at) VALUES
-- Sangotedo Area (Multiple variations)
(1, 'Sangotedo', 'sangotedo', ST_GeogFromText('POINT(3.6285 6.4698)'), 1000, NOW() - INTERVAL '30 days'),
(2, 'Sangotedo Phase 1', 'sangotedo phase 1', ST_GeogFromText('POINT(3.6300 6.4710)'), 1000, NOW() - INTERVAL '25 days'),
(3, 'Sangotedo Estate', 'sangotedo estate', ST_GeogFromText('POINT(3.6270 6.4685)'), 1000, NOW() - INTERVAL '20 days'),

-- Ikeja Area
(4, 'Ikeja GRA', 'ikeja gra', ST_GeogFromText('POINT(3.3515 6.6018)'), 1000, NOW() - INTERVAL '28 days'),
(5, 'Ikeja CBD', 'ikeja cbd', ST_GeogFromText('POINT(3.3500 6.6025)'), 1000, NOW() - INTERVAL '22 days'),
(6, 'Ikeja', 'ikeja', ST_GeogFromText('POINT(3.3490 6.6030)'), 1000, NOW() - INTERVAL '15 days'),

-- Lekki Area
(7, 'Lekki Phase 1', 'lekki phase 1', ST_GeogFromText('POINT(3.4616 6.4442)'), 1000, NOW() - INTERVAL '35 days'),
(8, 'Lekki', 'lekki', ST_GeogFromText('POINT(3.5780 6.4750)'), 1000, NOW() - INTERVAL '18 days'),

-- Victoria Island
(9, 'Victoria Island', 'victoria island', ST_GeogFromText('POINT(3.4210 6.4289)'), 1000, NOW() - INTERVAL '40 days'),
(10, 'VI', 'vi', ST_GeogFromText('POINT(3.4230 6.4275)'), 1000, NOW() - INTERVAL '12 days'),

-- Ajah Area
(11, 'Ajah', 'ajah', ST_GeogFromText('POINT(3.6400 6.4800)'), 1000, NOW() - INTERVAL '20 days'),
(12, 'Ajah Lagos', 'ajah lagos', ST_GeogFromText('POINT(3.6380 6.4780)'), 1000, NOW() - INTERVAL '10 days'),

-- Other Lagos Areas
(13, 'Surulere', 'surulere', ST_GeogFromText('POINT(3.3560 6.5010)'), 1000, NOW() - INTERVAL '25 days'),
(14, 'Yaba', 'yaba', ST_GeogFromText('POINT(3.3800 6.5150)'), 1000, NOW() - INTERVAL '22 days'),
(15, 'Ikoyi', 'ikoyi', ST_GeogFromText('POINT(3.4350 6.4520)'), 1000, NOW() - INTERVAL '30 days'),
(16, 'Apapa', 'apapa', ST_GeogFromText('POINT(3.3600 6.4480)'), 1000, NOW() - INTERVAL '35 days'),
(17, 'Maryland', 'maryland', ST_GeogFromText('POINT(3.3650 6.5750)'), 1000, NOW() - INTERVAL '15 days'),
(18, 'Ogba', 'ogba', ST_GeogFromText('POINT(3.3300 6.6200)'), 1000, NOW() - INTERVAL '20 days');

-- Reset sequence after manual ID insertion
SELECT setval('geo_geobucket_id_seq', (SELECT MAX(id) FROM geo_geobucket));

-- ============================================
-- 2. PROPERTIES - Sample Real Estate Listings
-- ============================================

INSERT INTO properties_property (id, title, location_name, location, price, bedrooms, bathrooms, geo_bucket_id, created_at) VALUES
-- =========== SANGOTEDO AREA PROPERTIES (3 buckets) ===========
-- Bucket 1: Sangotedo
(1, 'Luxury Villa Sangotedo', 'Sangotedo', ST_GeogFromText('POINT(3.6285 6.4698)'), 75000000, 5, 4, 1, NOW() - INTERVAL '5 days'),
(2, 'Modern Duplex Sangotedo', 'Sangotedo', ST_GeogFromText('POINT(3.6290 6.4700)'), 85000000, 6, 5, 1, NOW() - INTERVAL '4 days'),
(3, 'Affordable Bungalow Sangotedo', 'Sangotedo', ST_GeogFromText('POINT(3.6280 6.4695)'), 35000000, 3, 2, 1, NOW() - INTERVAL '3 days'),

-- Bucket 2: Sangotedo Phase 1
(4, 'Phase 1 Luxury Apartment', 'Sangotedo Phase 1', ST_GeogFromText('POINT(3.6305 6.4712)'), 65000000, 4, 3, 2, NOW() - INTERVAL '6 days'),
(5, 'Phase 1 Townhouse', 'Sangotedo Phase 1', ST_GeogFromText('POINT(3.6298 6.4708)'), 55000000, 4, 3, 2, NOW() - INTERVAL '7 days'),

-- Bucket 3: Sangotedo Estate
(6, 'Estate Mansion', 'Sangotedo Estate', ST_GeogFromText('POINT(3.6275 6.4688)'), 95000000, 7, 6, 3, NOW() - INTERVAL '2 days'),
(7, 'Estate Family Home', 'Sangotedo Estate', ST_GeogFromText('POINT(3.6268 6.4682)'), 45000000, 4, 3, 3, NOW() - INTERVAL '1 day'),

-- =========== IKEJA AREA PROPERTIES (3 buckets) ===========
-- Bucket 4: Ikeja GRA
(8, 'GRA Executive Duplex', 'Ikeja GRA', ST_GeogFromText('POINT(3.3520 6.6020)'), 120000000, 5, 4, 4, NOW() - INTERVAL '10 days'),
(9, 'GRA Mini Estate', 'Ikeja GRA', ST_GeogFromText('POINT(3.3510 6.6015)'), 180000000, 8, 6, 4, NOW() - INTERVAL '8 days'),

-- Bucket 5: Ikeja CBD
(10, 'CBD Office Space', 'Ikeja Central Business District', ST_GeogFromText('POINT(3.3505 6.6028)'), 300000000, 0, 10, 5, NOW() - INTERVAL '15 days'),
(11, 'CBD Commercial Plaza', 'Ikeja CBD', ST_GeogFromText('POINT(3.3495 6.6020)'), 500000000, 0, 15, 5, NOW() - INTERVAL '12 days'),

-- Bucket 6: Ikeja
(12, 'Ikeja Family House', 'Ikeja', ST_GeogFromText('POINT(3.3492 6.6035)'), 68000000, 4, 3, 6, NOW() - INTERVAL '9 days'),
(13, 'Ikeja Apartment Complex', 'Ikeja Lagos', ST_GeogFromText('POINT(3.3488 6.6030)'), 42000000, 3, 2, 6, NOW() - INTERVAL '7 days'),

-- =========== LEKKI AREA PROPERTIES (2 buckets) ===========
-- Bucket 7: Lekki Phase 1
(14, 'Lekki Waterfront Villa', 'Lekki Phase 1', ST_GeogFromText('POINT(3.4620 6.4445)'), 280000000, 7, 6, 7, NOW() - INTERVAL '20 days'),
(15, 'Phase 1 Luxury Penthouse', 'Lekki Phase 1', ST_GeogFromText('POINT(3.4610 6.4438)'), 350000000, 6, 5, 7, NOW() - INTERVAL '18 days'),

-- Bucket 8: Lekki
(16, 'Lekki Apartments', 'Lekki', ST_GeogFromText('POINT(3.5785 6.4755)'), 65000000, 3, 2, 8, NOW() - INTERVAL '5 days'),
(17, 'Lekki Townhouse', 'Lekki Lagos', ST_GeogFromText('POINT(3.5775 6.4748)'), 85000000, 4, 3, 8, NOW() - INTERVAL '4 days'),

-- =========== VICTORIA ISLAND AREA (2 buckets) ===========
-- Bucket 9: Victoria Island
(18, 'VI Luxury Penthouse', 'Victoria Island', ST_GeogFromText('POINT(3.4215 6.4292)'), 500000000, 5, 4, 9, NOW() - INTERVAL '30 days'),
(19, 'VI Executive Suite', 'Victoria Island Lagos', ST_GeogFromText('POINT(3.4205 6.4285)'), 320000000, 4, 3, 9, NOW() - INTERVAL '25 days'),

-- Bucket 10: VI (abbreviation)
(20, 'VI Office Tower', 'VI', ST_GeogFromText('POINT(3.4235 6.4278)'), 750000000, 0, 20, 10, NOW() - INTERVAL '22 days'),

-- =========== AJAH AREA (2 buckets) ===========
-- Bucket 11: Ajah
(21, 'Ajah Beach House', 'Ajah', ST_GeogFromText('POINT(3.6405 6.4805)'), 220000000, 6, 5, 11, NOW() - INTERVAL '14 days'),
(22, 'Ajah Family Home', 'Ajah Lagos', ST_GeogFromText('POINT(3.6395 6.4798)'), 95000000, 5, 4, 11, NOW() - INTERVAL '10 days'),

-- Bucket 12: Ajah Lagos
(23, 'Ajah Apartment Block', 'Ajah Lagos', ST_GeogFromText('POINT(3.6385 6.4785)'), 42000000, 3, 2, 12, NOW() - INTERVAL '8 days'),

-- =========== OTHER AREAS (6 buckets) ===========
-- Bucket 13: Surulere
(24, 'Surulere Townhouse', 'Surulere', ST_GeogFromText('POINT(3.3565 6.5015)'), 55000000, 3, 2, 13, NOW() - INTERVAL '12 days'),

-- Bucket 14: Yaba
(25, 'Yaba Student Apartment', 'Yaba Mainland', ST_GeogFromText('POINT(3.3805 6.5155)'), 28000000, 2, 1, 14, NOW() - INTERVAL '9 days'),

-- Bucket 15: Ikoyi
(26, 'Ikoyi Luxury Duplex', 'Ikoyi Lagos', ST_GeogFromText('POINT(3.4355 6.4525)'), 650000000, 5, 4, 15, NOW() - INTERVAL '28 days'),

-- Bucket 16: Apapa
(27, 'Apapa Warehouse', 'Apapa', ST_GeogFromText('POINT(3.3605 6.4485)'), 180000000, 0, 8, 16, NOW() - INTERVAL '20 days'),

-- Bucket 17: Maryland
(28, 'Maryland Bungalow', 'Maryland Ikeja', ST_GeogFromText('POINT(3.3655 6.5755)'), 75000000, 4, 3, 17, NOW() - INTERVAL '11 days'),

-- Bucket 18: Ogba
(29, 'Ogba Family House', 'Ogba Lagos', ST_GeogFromText('POINT(3.3305 6.6205)'), 48000000, 3, 2, 18, NOW() - INTERVAL '7 days'),

-- Additional properties for testing density
(30, 'Sangotedo Test Property 1', 'Sangotedo', ST_GeogFromText('POINT(3.6282 6.4702)'), 38000000, 2, 2, 1, NOW() - INTERVAL '2 hours'),
(31, 'Sangotedo Test Property 2', 'Sangotedo Phase 1', ST_GeogFromText('POINT(3.6302 6.4715)'), 42000000, 3, 2, 2, NOW() - INTERVAL '1 hour'),
(32, 'Ikeja Test Property', 'Ikeja', ST_GeogFromText('POINT(3.3498 6.6032)'), 52000000, 3, 2, 6, NOW());

-- Reset sequence after manual ID insertion
SELECT setval('properties_property_id_seq', (SELECT MAX(id) FROM properties_property));

-- ============================================
-- 3. STATISTICS QUERY - Verify Data
-- ============================================

-- Summary Statistics
SELECT
    'Bucket Statistics' as section,
    COUNT(DISTINCT gb.id) as total_buckets,
    COUNT(p.id) as total_properties,
    ROUND(AVG(p.price), 2) as avg_property_price,
    MIN(p.price) as min_price,
    MAX(p.price) as max_price
FROM geo_geobucket gb
LEFT JOIN properties_property p ON gb.id = p.geo_bucket_id;

-- Properties per Bucket Distribution
SELECT
    'Properties per Bucket' as section,
    gb.name as bucket_name,
    COUNT(p.id) as property_count,
    ROUND(AVG(p.price), 2) as avg_price_in_bucket
FROM geo_geobucket gb
LEFT JOIN properties_property p ON gb.id = p.geo_bucket_id
GROUP BY gb.id, gb.name
ORDER BY property_count DESC;

-- Top 5 Most Populated Buckets
SELECT
    'Top 5 Most Populated Buckets' as section,
    gb.name,
    COUNT(p.id) as property_count,
    STRING_AGG(p.title, ', ') as sample_properties
FROM geo_geobucket gb
JOIN properties_property p ON gb.id = p.geo_bucket_id
GROUP BY gb.id, gb.name
ORDER BY property_count DESC
LIMIT 5;

-- Price Distribution by Area
SELECT
    'Price Distribution by Area' as section,
    CASE
        WHEN gb.name ILIKE '%sangotedo%' THEN 'Sangotedo Area'
        WHEN gb.name ILIKE '%ikeja%' THEN 'Ikeja Area'
        WHEN gb.name ILIKE '%lekki%' THEN 'Lekki Area'
        WHEN gb.name ILIKE '%victoria%' OR gb.name ILIKE '%vi%' THEN 'VI Area'
        ELSE 'Other Areas'
    END as area_group,
    COUNT(p.id) as property_count,
    ROUND(AVG(p.price), 2) as avg_price,
    ROUND(MIN(p.price), 2) as min_price,
    ROUND(MAX(p.price), 2) as max_price
FROM geo_geobucket gb
JOIN properties_property p ON gb.id = p.geo_bucket_id
GROUP BY area_group
ORDER BY avg_price DESC;

-- ============================================
-- 4. TEST SEARCH SCENARIOS - Verify Functionality
-- ============================================

-- Test 1: Find all Sangotedo properties (should return 7 properties across 3 buckets)
SELECT 'Test 1: Sangotedo Search' as test_scenario;
SELECT p.title, p.location_name, gb.name as bucket_name, p.price
FROM properties_property p
JOIN geo_geobucket gb ON p.geo_bucket_id = gb.id
WHERE gb.normalized_name ILIKE '%sangotedo%'
ORDER BY p.price DESC;

-- Test 2: Find properties within 2km of Sangotedo center
SELECT 'Test 2: Radius Search from Sangotedo (2km)' as test_scenario;
SELECT p.title,
       ST_Distance(p.location::geography, ST_GeogFromText('POINT(3.6285 6.4698)')) as distance_meters,
       p.location_name,
       p.price
FROM properties_property p
WHERE ST_Distance(p.location::geography, ST_GeogFromText('POINT(3.6285 6.4698)')) <= 2000
ORDER BY distance_meters;

-- Test 3: Check bucket efficiency (buckets with > 2 properties)
SELECT 'Test 3: Bucket Efficiency' as test_scenario;
SELECT gb.name as bucket_name,
       COUNT(p.id) as property_count,
       CASE
           WHEN COUNT(p.id) >= 5 THEN 'Highly Efficient'
           WHEN COUNT(p.id) >= 2 THEN 'Efficient'
           WHEN COUNT(p.id) = 1 THEN 'Underutilized'
           ELSE 'Empty'
       END as efficiency_status
FROM geo_geobucket gb
LEFT JOIN properties_property p ON gb.id = p.geo_bucket_id
GROUP BY gb.id, gb.name
ORDER BY property_count DESC;

-- ============================================
-- 5. CREATE TEST USERS (Optional)
-- ============================================

-- Note: Uncomment and modify if you need test users
/*
INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined)
VALUES
('test_agent', 'agent@example.com', 'pbkdf2_sha256$...', true, false, true, NOW()),
('test_buyer', 'buyer@example.com', 'pbkdf2_sha256$...', false, false, true, NOW());
*/

-- ============================================
-- SCRIPT COMPLETE MESSAGE
-- ============================================
SELECT '✅ Seed data successfully inserted!' as message;
SELECT 'Total Buckets: ' || COUNT(*) as bucket_count FROM geo_geobucket;
SELECT 'Total Properties: ' || COUNT(*) as property_count FROM properties_property;