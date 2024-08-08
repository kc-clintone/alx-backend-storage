-- This script creates a trigger to automatically decrease the quantity of an item in the 'items' table after a new order is added.

DELIMITER $$

CREATE TRIGGER decrease_item_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.quantity_ordered
    WHERE item_id = NEW.item_id;
END $$

DELIMITER ;

