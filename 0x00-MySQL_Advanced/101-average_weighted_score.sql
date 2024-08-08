-- This script creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and stores the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE total_weighted_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE current_user_id INT;

    -- Declare a cursor to iterate over all user IDs
    DECLARE user_cursor CURSOR FOR
    SELECT id FROM users;

    -- Declare a handler to exit the loop when no more rows are found
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open the cursor
    OPEN user_cursor;

    user_loop: LOOP
        -- Fetch each user ID
        FETCH user_cursor INTO current_user_id;

        -- Exit the loop if no more rows
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Reset variables for each user
        SET total_weighted_score = 0;
        SET total_weight = 0;

        -- Calculate the total weighted score for the current user
        SELECT
            SUM(corrections.score * projects.weight)
        INTO
            total_weighted_score
        FROM
            corrections
        INNER JOIN
            projects ON corrections.project_id = projects.id
        WHERE
            corrections.user_id = current_user_id;

        -- Calculate the total weight for the current user
        SELECT
            SUM(projects.weight)
        INTO
            total_weight
        FROM
            corrections
        INNER JOIN
            projects ON corrections.project_id = projects.id
        WHERE
            corrections.user_id = current_user_id;

        -- Update the average score in the users table for the current user
        IF total_weight = 0 THEN
            UPDATE users
            SET average_score = 0
            WHERE id = current_user_id;
        ELSE
            UPDATE users
            SET average_score = total_weighted_score / total_weight
            WHERE id = current_user_id;
        END IF;

    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END $$

DELIMITER ;
