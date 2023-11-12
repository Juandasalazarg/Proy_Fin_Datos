----------------------------------------------------TABLE MAKER-------------------------------

create table Maker(
	Id_Maker Serial,
	Maker_Name varchar(20),
	primary key(Id_Maker));
	
copy Maker from 'C:\Users\Public\Documents\Fabricantes.csv' delimiter ';' csv header;

select * from Maker

----------------------------------------------------TABLE COUNTY-------------------------------

create table County(
	Id_county Serial,
	County_Name varchar(20),
	primary key(Id_county));

copy County from 'C:\Users\Public\Documents\Condados.csv' delimiter ';' csv header;

Select * from County
----------------------------------------------------TABLE CITY-------------------------------

create table City(
	Id_county Serial,
	City_Name varchar(40),
	Legislative_district integer,
	foreign key(Id_county) references County);

copy City from 'C:\Users\Public\Documents\Ciudades.csv' delimiter ';' csv header;

select * from City

----------------------------------------------------TABLE CENSUS_TRACK-------------------------------
create table Census_Track(
	Census_Id numeric(11),
	Id_county Serial,
	City_Name varchar(40),
	foreign key(Id_county) references County);
	
copy Census_Track from 'C:\Users\Public\Documents\Census_track.csv' delimiter ';' csv header;

select * from  Census_Track

----------------------------------------------------TABLE ELECTRIC-CARS-MODELS-------------------------------
create table Electric_Cars_Models(
	Id_maker integer,
	Model_name varchar(30),
	primary key(Model_name),
	foreign key(Id_maker) references Maker);

copy Electric_Cars_Models from 'C:\Users\Public\Documents\Modelos_Carros_Electricos.csv' delimiter ';' csv header;

select * from  Electric_Cars_Models


----------------------------------------------------TABLE ELECTRIC-CARS-TYPE-------------------------------
create table Electric_Cars_Type(
	Model_year integer,
	Id_maker integer,
	Car_Model_name varchar(30),
	Electric_type varchar(38),
	Clean_Alternative_Fuel_Vehicle varchar(60),
	Electric_range varchar(10),
	foreign key(Car_Model_name) references Electric_Cars_Models ,
	foreign key(Id_maker) references Maker);

copy Electric_Cars_Type from 'C:\Users\Public\Documents\Electric_type.csv' delimiter ';' csv header;

select * from  Electric_Cars_Type


----------------------------------------------------TABLE DOL_ID-------------------------------
create table Dol_Id(
	DOL_Vehicle numeric(10),
	State varchar(2) CHECK (State = 'WA'),
	Postal_Code integer,
	Census_track numeric(12),
	primary key(DOL_Vehicle));



copy Dol_Id from 'C:\Users\Public\Documents\Dol_id.csv' delimiter ';' csv header;

select * from Dol_Id


----------------------------------------------------TABLE VEHICLES-------------------------------
create table Vehicle(
	DOL_Vehicle numeric(10),
	Vehicle_ID_VIN varchar(10),
	Id_county integer,
	City_Name varchar(40),
	Model_year integer,
	Id_maker integer,
	Car_Model_name varchar(30),
	Electric_type varchar(38),
	Vehicle_Location varchar(60),
	Electric_utility varchar(150),
	foreign key(DOL_Vehicle) references Dol_Id,
	foreign key(Id_county) references County,
	foreign key(Car_Model_name) references Electric_Cars_Models ,
	foreign key(Id_maker) references Maker);

drop table Vehicle
copy Vehicle from 'C:\Users\Public\Documents\Vehicles.csv' delimiter ';' csv header;

select * from Vehicle



