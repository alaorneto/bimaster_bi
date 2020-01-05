CREATE DATABASE sa;
CREATE TABLE favorecidos (
  cnpj varchar(14) PRIMARY KEY,
  atividadePrincipal varchar(300),
  uf varchar(2),
  cidade varchar(100)
);

select * from favorecidos;
