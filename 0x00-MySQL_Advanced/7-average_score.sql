-- This script creates a stored procedure ComputeAverageScoreForUser that computes and stores the average score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Step 1: Calculate the average score for the given user_id
    SELECT AVG(score)
    INTO avg_score
    FROM corrections
    WHERE user_id = p_user_id;

    -- Step 2: Update the average_score in the users table
    UPDATE users
    SET average_score = avg_score
    WHERE id = p_user_id;
END $$

DELIMITER ;

