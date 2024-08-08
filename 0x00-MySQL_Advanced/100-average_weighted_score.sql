-- This script creates a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE avg_weighted_score INT DEFAULT 0;

    -- Step 1: Calculate the average weighted score for the given user_id
    SELECT
        SUM(score * weight) / SUM(weight) INTO avg_weighted_score
    FROM
        corrections
    WHERE
        user_id = p_user_id;

    -- Step 2: Update the average_weighted_score in the users table
    UPDATE users
    SET average_weighted_score = avg_weighted_score
    WHERE id = p_user_id;
END $$

DELIMITER ;

