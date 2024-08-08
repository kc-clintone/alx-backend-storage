-- This script ranks country origins of metal bands based on the total number of non-unique fans.
-- Step 1: Import the metal_bands table (assume it is already imported and available in the database).
-- Step 2: Query to rank the country origins based on the total number of fans.

SELECT
    origin,
    SUM(nb_fans) AS total_fans
FROM
    metal_bands
GROUP BY
    origin
ORDER BY
    total_fans DESC;
