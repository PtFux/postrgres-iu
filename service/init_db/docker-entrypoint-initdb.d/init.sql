-- init.sql

create database prof_iu;
create user predsed with encrypted password 'predsed_profa_iu_3301';
grant all privileges on database prof_iu to predsed;
