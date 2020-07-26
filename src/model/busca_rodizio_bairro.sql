select tb1.data_inicio, tb1.data_fim, tb2.cidade, tb3.bairro, tb4.area from rodizio as tb1
    join cidades as tb2 
        on tb1.cidade_id = tb2.id
    join bairros as tb3
        on tb1.bairro_id = tb3.id
    join areas as tb4
        on tb1.area_id = tb4.id
    where tb2.cidade = '{cidade}'
    and tb3.bairro = '{bairro}'
    and tb1.data_inicio > '{dt_inicio}'
    order by tb1.data_inicio;
