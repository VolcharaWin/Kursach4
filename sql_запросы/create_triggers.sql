CREATE OR REPLACE FUNCTION check_dateout() 
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, что дата выселения позже даты заселения
    IF NEW."ZasDateIN" >= NEW."ZasDateOUT" THEN
        RAISE EXCEPTION 'Ошибка! Дата выселения не может быть раньше даты заселения';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER DateOUT
AFTER INSERT ON Zaselenie
FOR EACH ROW
EXECUTE FUNCTION check_dateout();

CREATE OR REPLACE FUNCTION check_datein()
RETURNs TRIGGER AS $$
BEGIN
	-- Проверяем, что дата заселения меньше, чем текущая дата
	IF NEW."ZasDateIn" <= CURRENT_TIMESTAMP THEN
		RAISE EXCEPTION 'Ошибка! Дата заселения не может быть меньше текущей даты';
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER DateIN
AFTER INSERT ON Zaselenie
FOR EACH ROW
EXECUTE FUNCTION check_datein();

CREATE OR REPLACE FUNCTION check_zas_cond()
RETURNs TRIGGER AS $$
DECLARE
	overlap_count integer;
BEGIN
	--Проверка пересечения дат заселения и выселения для одного и того же номера
	SELECT COUNT(*)
	INTO overlap_count
	FROM Zaselenie z
	WHERE z."NomID" = NEW."NomID"
	AND NEW."ZasDateIn" <= z."ZasDateOut";
	--Если найдено пересечение, то выбрасываем исключение
	IF overlap_count > 0 THEN
		RAISE EXCEPTION 'Ошибка! Номер не будет готов для заселения!';
	END IF;

	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ZasCond
AFTER INSERT ON Zaselenie
FOR EACH ROW
EXECUTE FUNCTION check_zas_cond();

CREATE OR REPLACE FUNCTION check_pusl_avail()
RETURNS TRIGGER AS $$
DECLARE
    unavailable_count INT;
BEGIN
    -- Проверка доступности услуги для заселения
    SELECT COUNT(*)
    INTO unavailable_count
    FROM Zaselenie z
    JOIN PredUslug p ON p."PuslID" = z."PuslID"
    WHERE NEW."PuslID" = z."PuslID" 
    AND p."PuslAvail" = 0;

    -- Если услуга недоступна, выбрасываем исключение
    IF unavailable_count > 0 THEN
        RAISE EXCEPTION 'Данная услуга недоступна!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER PuslAvail
AFTER INSERT ON Zaselenie
FOR EACH ROW
EXECUTE FUNCTION check_pusl_avail();
