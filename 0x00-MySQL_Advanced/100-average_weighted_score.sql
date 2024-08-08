-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE total_weighted_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the total weighted score for the given user
    SELECT
        SUM(corrections.score * projects.weight)
    INTO
        total_weighted_score
    FROM
        corrections
    INNER JOIN
        projects ON corrections.project_id = projects.id
    WHERE
        corrections.user_id = p_user_id;

    -- Calculate the total weight for the given user
    SELECT
        SUM(projects.weight)
    INTO
        total_weight
    FROM
        corrections
    INNER JOIN
        projects ON corrections.project_id = projects.id
    WHERE
        corrections.user_id = p_user_id;

    -- Update the average score in the users table
    IF total_weight = 0 THEN
        UPDATE users
        SET average_score = 0
        WHERE id = p_user_id;
    ELSE
        UPDATE users
        SET average_score = total_weighted_score / total_weight
        WHERE id = p_user_id;
    END IF;
END $$

DELIMITER ;

