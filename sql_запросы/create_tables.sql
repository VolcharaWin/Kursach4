CREATE TABLE Clienti(
ClientID integer NOT NULL,
ClientFIO varchar(50) NOT NULL,
CLientBD date NOT NULL,
ClientPass varchar(50) not null,
CONSTRAINT Clienti_PK PRIMARY KEY (ClientID));

CREATE TABLE DopUslugi(
DuslID integer NOT NULL,
DuslName varchar(50) NOT NULL,
DuslPrice numeric(10, 2) NOT NULL,
CONSTRAINT DopUslugi_PK PRIMARY KEY (DuslID));

CREATE TABLE Personal(
PersID integer NOT NULL,
PersFIO varchar(50) NOT NULL,
PersDol varchar(50) NOT NULL,
CONSTRAINT Personal_PK PRIMARY KEY (PersID));

CREATE TABLE PredUslug(
PuslID integer NOT NULL,
PuslAvail bit NOT NULL,
DuslID int NOT NULL,
PersID int NOT NULL,
CONSTRAINT PredUslug_PK PRIMARY KEY  (PuslID),
CONSTRAINT PredUslug_DopUslugi_FK FOREIGN KEY (DuslID)
REFERENCES DopUslugi (DuslID));

CREATE TABLE Nomera(
NomID integer NOT NULL,
NomPrice numeric(10, 2) NOT NULL,
NomMesta integer NOT NULL,
PersID integer NOT NULL,
CONSTRAINT Nomera_PK PRIMARY KEY (NomID),
CONSTRAINT Nomera_Personal_FK FOREIGN KEY (PersID)
REFERENCES Personal (PersID));

CREATE TABLE Zaselenie(
ZasID integer NOT NULL,
ZasDateIN TIMESTAMP WITH TIME ZONE NOT NULL,
ZasDateOUT TIMESTAMP WITH TIME ZONE NOT NULL,
PuslID integer NULL,
ClientID integer NOT NULL,
NomID integer NOT NULL,
PersID integer NOT NULL,
CONSTRAINT Zaselenie_PK PRIMARY KEY (ZasID),
CONSTRAINT Zaselenie_Personal_FK FOREIGN KEY (PersID)
REFERENCES Personal (PersID),
CONSTRAINT Zaselenie_Nomera_FK FOREIGN KEY (NomID)
REFERENCES Nomera (NomID),
CONSTRAINT Zaselenie_Clienti_FK FOREIGN KEY (ClientID)
REFERENCES Clienti (ClientID),
CONSTRAINT Zaselenie_PredUslug_FK FOREIGN KEY (PuslID)
REFERENCES PredUslug (PuslID));

CREATE TABLE Projiv(
ProjID integer NOT NULL,
ProjFIO varchar(50) NOT NULL,
ProjBD TIMESTAMP WITH TIME ZONE NOT NULL,
ProjPass varchar(50) NOT NULL,
ZasID integer NOT NULL,
CONSTRAINT Projiv_PK PRIMARY KEY (ProjID),
CONSTRAINT Projiv_Zaselenie_FK FOREIGN KEY (ZasID)
REFERENCES Zaselenie (ZasID));
