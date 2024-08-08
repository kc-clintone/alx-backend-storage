-- This script lists all bands with Glam rock as their main style, ranked by their longevity (lifespan in years).
-- Step 1: Query to list Glam rock bands and calculate their lifespan.

SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
    ORDER BY lifespan DESC;
