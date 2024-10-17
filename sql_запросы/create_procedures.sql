CREATE OR REPLACE PROCEDURE add_clienti(
    p_id integer,
    p_fio varchar(50),
    p_bd date,
    p_pass varchar(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Clienti(ClientID, ClientFIO, ClientBD, ClientPass)
    VALUES (p_id, p_fio, p_bd, p_pass);
END;
$$;
CREATE OR REPLACE PROCEDURE add_Personal(
    p_id integer,
    p_fio varchar(50),
    p_dol varchar(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Personal(PersID, PersFIO, PersDol)
	VALUES(p_id, p_fio, p_dol);
END;
$$;
CREATE OR REPLACE PROCEDURE add_Nomera(
    p_id integer,
    p_Price numeric(10, 2),
    p_Mesta varchar(50),
	p_PersID integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Nomera(NomID, NomPrice, NomMesta, PersID)
	VALUES(p_id, p_Price, p_Mesta, p_PersID);
END;
$$;
CREATE OR REPLACE PROCEDURE add_DopUslugi(
    p_id integer,
    p_Name varchar(50),
    p_Price numeric(10, 2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO DopUslugi(DuslID, DuslName, DuslPrice)
	VALUES(p_id, p_Name, p_Price);
END;
$$;
CREATE OR REPLACE PROCEDURE add_PredUslugi(
    p_id integer,
	p_avail bit,
	p_duslid integer,
	p_persid integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO PredUslug(PuslID, PuslAvail, DuslID, PersID)
	VALUES(p_id, p_avail, p_duslid, p_persid);
END;
$$;
CREATE OR REPLACE PROCEDURE add_Zaselenie(
    p_id integer,
	p_in TIMESTAMP WITH TIME ZONE,
	p_out TIMESTAMP WITH TIME ZONE,
	p_puslid integer,
	p_clientid integer,
	p_nomid integer,
	p_persid integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Zaselenie(ZasID, ZasDateIN, ZasDateOUT, PuslID, ClientID, NomID, PersID)
	VALUES(p_id, p_in, p_out, p_puslid, p_clientid, p_nomid, p_persid);
END;
$$;
CREATE OR REPLACE PROCEDURE add_Projiv(
    p_id integer,
	p_fio varchar(50),
	p_bd date,
	p_pass varchar(50),
	p_zasid integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Projiv(ProjID, ProjFIO, ProjBD, ProjPass, ZasID)
	VALUES(p_id, p_fio, p_bd, p_pass, p_zasid);
END;
$$;
CREATE OR REPLACE PROCEDURE ZasDate(
	p_id integer,
	p_out TIMESTAMP WITH TIME ZONE 
)
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE Zaselenie SET ZasDateOUT = p_out WHERE ZasID = p_id;
END;
$$;
CREATE OR REPLACE PROCEDURE up_projiv(
	p_id integer,
	p_zasid integer 
)
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE Projiv SET ZasID = p_zasid WHERE ProjID = p_id;
END;
$$;