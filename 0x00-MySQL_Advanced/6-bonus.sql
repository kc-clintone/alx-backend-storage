-- This script creates a stored procedure AddBonus that adds a new correction for a student, creating the project if it doesn't already exist.

DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Step 1: Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = p_project_name
    LIMIT 1;

    -- Step 2: If project does not exist, create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (p_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Step 3: Insert the new correction
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (p_user_id, project_id, p_score);
END $$

DELIMITER ;
