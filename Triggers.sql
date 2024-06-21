Use Project;
DELIMITER //

CREATE TRIGGER BeforeInsertUserPromotion
BEFORE INSERT ON UserPromotions FOR EACH ROW
BEGIN
    DECLARE validFrom DATE;
    DECLARE validTill DATE;
    
    SELECT ValidFrom, ValidTill INTO validFrom, validTill
    FROM Promotions
    WHERE PromoID = NEW.PromoID;
    
    IF NEW.DateUsed < validFrom OR NEW.DateUsed > validTill THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The date used is outside the valid promotion period.';
    END IF;
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER CheckAgeBeforeInsert
BEFORE INSERT ON Users
FOR EACH ROW
BEGIN
    IF NEW.DateOfBirth > CURRENT_DATE - INTERVAL 18 YEAR THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User must be at least 18 years old.';
    END IF;
END;
//

CREATE TRIGGER CheckAgeBeforeUpdate
BEFORE UPDATE ON Users
FOR EACH ROW
BEGIN
    IF NEW.DateOfBirth > CURRENT_DATE - INTERVAL 18 YEAR THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User must be at least 18 years old.';
    END IF;
END;
//

DELIMITER ;



