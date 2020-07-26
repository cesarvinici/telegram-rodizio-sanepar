-- select * from rodizio where data_inicio = '2020-07-22 04:00' and data_fim = '2020-07-24 04:00' and cidade_id = 3 and bairro_id = 238 and area_id = 56;
select tb1.data_inicio, tb1.data_fim, tb2.cidade, tb3.bairro, tb4.area from rodizio as tb1
    join cidades as tb2 
        on tb1.cidade_id = tb2.id
    join bairros as tb3
        on tb1.bairro_id = tb3.id
    join areas as tb4
        on tb1.area_id = tb4.id
    where data_inicio > "2020-07-22";


select tb1.cidade, count(tb2.bairro) as 'qtd_bairro' from cidades as tb1
    join bairros as tb2
        on tb1.id = tb2.cidade_id
    GROUP BY tb1.cidade order by count(tb2.bairro) desc;


select min(data_inicio), MAX(data_inicio) from rodizio;



SELECT bairro from bairros as b join cidades c on c.id = b.cidade_id where c.cidade = 'curitiba' order by bairro asc;


select * from rodizio where data_inicio  BETWEEN "2020-07-22 00:00" and "2020-07-22 23:59";

select count(*) from rodizio where data_inicio like "%2020-07-22%";

-- delete from rodizio where data_inicio like "%2020-07-22%";


-- update bairros set bairro = 'água verde' where id = 81;