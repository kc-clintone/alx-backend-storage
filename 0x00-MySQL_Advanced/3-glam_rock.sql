-- This script lists all bands with Glam rock as their main style, ranked by their longevity (lifespan in years).
-- Step 1: Query to list Glam rock bands and calculate their lifespan.

SELECT
    band_name,
    CASE
        WHEN split IS NOT NULL THEN split - formed
        ELSE 2020 - formed
    END AS lifespan
FROM
    metal_bands
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC;
