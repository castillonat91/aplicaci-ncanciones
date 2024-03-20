CREATE DATABASE AGENDA2024;
use AGENDA2024;

create table Personas(
idper int primary key auto_increment,
nombreper varchar(60) not null,
apellidoper varchar(60) not null,
emailper varchar(60) not null,
dirper varchar(60) not null,
telper varchar(60) not null,
usuarioper varchar(60) not null,
contraper varchar(255) not null
);
alter table Personas add roles varchar(60);
CREATE TABLE canciones(
	id_can int auto_increment primary key,
    titulo varchar(60) not null,
    artista varchar(60) not null,
    genero varchar(60) not null,
    lanzamiento date not null,
    precio VARCHAR(60) not null,
    duracion varchar(60) not null,
    imagen BLOB

);
describe Personas;
describe canciones;
describe Personas;
select * from Personas;

