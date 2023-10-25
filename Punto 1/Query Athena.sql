SELECT 
cast(date_parse(SUBSTRING(fecha,1,10),'%d/%m/%Y') as date) as fecha, 
avg(precio) as precio, 
count(precio) as cant_registros
FROM "AwsDataCatalog"."banrep"."final" 
group by date_parse(SUBSTRING(fecha,1,10),'%d/%m/%Y')
order by fecha
