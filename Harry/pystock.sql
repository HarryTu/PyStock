create table stocks(
code varchar(7),
codealias varchar(10),
name varchar(30),
scope varchar(50),
circulated float,
totalstock float,
status int,
peg float,
lyr float,
mtime datetime
);

alter table stocks add primary key(code);


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
price float,
initchangeratio float,
changeratio float,
amountp float,
amountn float,
mtime datetime,
inittime datetime		
);

alter table mystocks add primary key(code);

create table rtstocks(
code varchar(7),
cashin float,
cashout float,
netvalue float,
iorate float,
turnover float,
price float,
changeratio float,
amountp float,
amountn float,
mtime datetime		
);

alter table rtstocks add primary key(code,time);
