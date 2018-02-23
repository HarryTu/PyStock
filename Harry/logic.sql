
select a.code, a.name, a.industry, b.initprice, b.price, c.netvalue, c.amountp, b.changeratio, c.changeratio, d.changeratio, c.turnover, d.turnover, d.netvalue, d.amountp, d.qrratio, (b.price/b.initprice) as ratio
from stocks a, jjtemp b, jjstocks c, rtstocks d
where a.code = b.code and b.code=c.code and a.code=d.code and b.price > b.initprice 
and c.netvalue >0 and c.amountp > 200 and c.mtime >= str_to_date('2018-02-23','%Y-%m-%d') and d.mtime >= str_to_date('2018-02-23','%Y-%m-%d') 
and (b.price/b.initprice) > 1.005 and  ( ( c.changeratio < 5 and c.changeratio > -4 ) or (c.changeratio < 6 and c.changeratio > -4 and (b.price/b.initprice) > 1.02 ) )
