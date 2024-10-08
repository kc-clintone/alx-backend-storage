-- This script creates a function SafeDiv that divides the first number by the second or returns 0 if the second number is 0.

DELIMITER $$

CREATE FUNCTION SafeDiv(
    a INT,
    b INT
)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE res FLOAT DEFAULT 0;

    -- Check if the divisor is zero
    IF b = 0 THEN
        RETURN 0;
    ELSE
        SET res = a / b;
    END IF;
    RETURN res;
END $$

DELIMITER ;

