create database cadastro_produtos;  
use cadastro_produtos;

create table produtos(
id INT NOT NULL AUTO_INCREMENT,
codigo int,
produto varchar(50),
quantidade int,
categoria varchar(20),
PRIMARY KEY (id)
);  

describe produtos;

select * from produtos;

