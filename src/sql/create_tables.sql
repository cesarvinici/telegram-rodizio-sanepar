-- Create Cidades
drop TABLE IF EXISTS cidades;
create table cidades (id INTEGER PRIMARY KEY, cidade TEXT);
-- Create Bairros
drop table if EXISTS bairros;
CREATE TABLE bairros (id integer PRIMARY KEY, cidade_id integer, bairro text);
-- Create Areas
drop table if EXISTS areas;
CREATE TABLE areas (id integer PRIMARY KEY, area text);
--create rodizio
drop table if EXISTS rodizio;
CREATE TABLE rodizio (id INTEGER PRIMARY KEY, data_inicio DATETIME, data_fim DATETIME, cidade_id INTEGER, bairro_id integer, area_id integer NULL);


