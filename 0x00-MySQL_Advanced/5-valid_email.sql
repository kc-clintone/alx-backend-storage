-- This script creates a trigger that resets the valid_email attribute to FALSE when the email has been changed.

DELIMITER $$

CREATE TRIGGER reset_valid_email_after_change
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = FALSE;
    END IF;
END $$

DELIMITER ;

