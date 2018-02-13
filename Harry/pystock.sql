create table stocks(
code varchar(7),
codealias varchar(10),
name varchar(30),
status int,
scope varchar(50),
circulated float,
totalstock float,
peg float,
lyr float,
mtime datetime
);

alter table stocks add primary key(code);

create table rtstocks(
code varchar(7),
cashin float,
cashout float,
netvalue float,
iorate float,
turnover float,
qrratio float,
price float,
changeratio float,
amountp float,
amountn float,
mystatus int,
mtime datetime

);

alter table rtstocks add primary key(code,mtime);


create table jjstocks(
code varchar(7),
cashin float,
cashout float,
netvalue float,
turnover float,
qrratio float,
price float,
changeratio float,
amountp float,
amountn float,
mtime datetime		
);

alter table jjstocks add primary key(code,mtime);


create table jjtemp(
code varchar(7),
codealias varchar(10),
initprice float, 
price float,
initturnover float, 
turnover float,
mtime datetime
)


create table mystocks(
code varchar(7),
codealias varchar(10),
name varchar(10),
cashin float,
cashout float,
initnetvalue float,
netvalue float,
iorate float,
turnover float,
qrratio float,
price float,
initchangeratio float,
changeratio float,
amountp float,
amountn float,
mtype int,					
mtime datetime,
inittime datetime
);

alter table mystocks add primary key(code,mtype);


create table hisstocks(
code varchar(7),
cashin float,
cashout float,
netvalue float,
iorate float,
turnover float,
qrratio float,
price float,
changeratio float,
amountp float,
amountn float,
mtime datetime		
);

alter table hisstocks add primary key(code,mtime);