import re
import time
import logging
import os
from scrapping.scrapy import Scraping
from sqlalchemy import create_engine
from datetime import datetime
from model import DAO

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(CURRENT_DIR, "log")
logging.basicConfig(filename=os.path.join(LOG_DIR, "file.log"), level=logging.INFO)

def altera_data(date_time: str) -> datetime:
    """
    Altera a string de data no formato dia/mes hora para o formato datetime do python \n
    :param date_time: str
    :return: report_date: datetime
    """
    date = date_time.split("-")[0].strip()
    time = date_time.split("-")[1].strip()
    report_date = datetime.strptime(date, "%d/%m")
    today = datetime.today()

    if today.month == 12 and report_date.month == 1:
        new_year = today.year + 1
        report_date = report_date.replace(year=new_year,
                                          hour=int(time.split(":")[0]),
                                          minute=int(time.split(":")[1]))
    else:
        report_date = report_date.replace(year=today.year,
                                          hour=int(time.split(":")[0]),
                                          minute=int(time.split(":")[1]))
    return report_date


def busca_cidade(cidade: str) -> int:
    """
    Verifica se a cidade ja existe no banco, caso o contrario, salva
    :param cidade: str
    :return: cidade_id: int
    """
    conn = DAO.db_connect()
    query_get_cidade = f"Select id from cidades where cidade = '{cidade}'"
    query_insert_cidade = f"insert into cidades (cidade) values ('{cidade}')"
    query = conn.execute(query_get_cidade)
    query_result = query.fetchone()
    try:
        cidade_id = query_result['id']
    except Exception:
        conn.execute(query_insert_cidade)
        cidade_id = conn.execute(query_get_cidade).fetchone()['id']

    return cidade_id


def busca_bairro(cidade_id: int, bairro: str) -> int:
    """
    Verifica se um bairro já existe para determinada cidade, caso contrario, salva no banco \n
    :param cidade_id: int
    :param bairro: str
    :return: bairro_id: int
    """
    conn = DAO.db_connect()
    query_get_bairro = f"Select id from bairros where cidade_id = {cidade_id} and bairro = '{bairro}'"
    query_insert_bairro = f"insert into bairros (cidade_id, bairro) values ({cidade_id}, '{bairro}')"
    query = conn.execute(query_get_bairro)
    query_result = query.fetchone()
    try:
        cidade_id = query_result['id']
    except Exception:
        conn.execute(query_insert_bairro)
        cidade_id = conn.execute(query_get_bairro).fetchone()['id']

    return cidade_id


def busca_area(area: str):
    """
    Verifica se uma área já existe no banco de dados, caso contrario, salva \n
    :param area: str
    :return: area_id: int
    """
    conn = DAO.db_connect()
    query_get_area = f"Select id from areas where area = '{area}'"
    query_insert_area = f"insert into areas (area) values ('{area}')"
    query = conn.execute(query_get_area)
    query_result = query.fetchone()
    try:
        area_id = query_result['id']
    except Exception:
        conn.execute(query_insert_area)
        area_id = conn.execute(query_get_area).fetchone()['id']

    return area_id


def area_iterate(registro: list):
    if 'area' in registro.keys():
        search_area = re.search("((Área.*)|(área.*))", registro['area'])
        if search_area:
            return busca_area(search_area.group(0).strip())


def salva_rodizio(data_inicio: datetime, data_fim: datetime, cidade_id: int, bairro_id: int, area_id: int):
    """
    Verifica se a informação de rodizio para uma determinada hora e lugar já existe no banco,
    caso contrario grava o registro \n
    :param data_inicio: datetime
    :param data_fim:  datetime
    :param cidade_id: int
    :param bairro_id: int
    :param area_id: int
    :return: None
    """
    conn = DAO.db_connect()
    date_format = "%Y-%m-%d %I:%M"

    search_query = """select * from rodizio where data_inicio = '{}'
                                            and data_fim = '{}'
                                            and cidade_id = {}
                                            and bairro_id = {}
                                            """
    if area_id:
        search_query = search_query + " and area_id = {}"

    query = conn.execute(search_query.format(
        data_inicio.strftime(date_format).strip(),
        data_fim.strftime(date_format).strip(),
        cidade_id,
        bairro_id,
        area_id))
    response = query.fetchall()
    if not response:
        if area_id:
            insert_query = """insert into rodizio (data_inicio, 
                                    data_fim, 
                                    cidade_id, 
                                    bairro_id, 
                                    area_id) 
                            values ('{}','{}', {}, {}, {})
                            """
            conn.execute(insert_query.format(
                data_inicio.strftime(date_format).strip(),
                data_fim.strftime(date_format).strip(),
                cidade_id,
                bairro_id,
                area_id
            ))
        else:
            insert_query = """insert into rodizio (data_inicio, 
                                    data_fim, 
                                    cidade_id, 
                                    bairro_id) 
                            values ('{}','{}', {}, {})
                            """
            conn.execute(insert_query.format(
                data_inicio.strftime(date_format).strip(),
                data_fim.strftime(date_format).strip(),
                cidade_id,
                bairro_id,
                area_id
            ))


def main():
    today = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    logging.info(f"{today} - INICIANDO SCRAPPING DOS DADOS.")
    data = Scraping()
    dados = data.get_scrapy()
    logging.info(f"{today} - TRATANDO OS DADOS E SALVANDO NO BANCO.")
    for registro in dados:
        data_inicio = altera_data(registro['inicio'])
        data_fim = altera_data(registro['fim'])
        cidade_id = busca_cidade(registro['cidade'].strip().lower())

        area_id = area_iterate(registro)

        for bairro in registro['bairros']:
            bairro = bairro.strip().replace(".", "")
            match = re.match("(?:([a-zA-ZzáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s]){1,})", bairro)

            if match:
                bairro = bairro[0:match.end()].strip()
                tem_separacao = re.search("([a-z\s]) e ([A-Z\s])", bairro)
                if tem_separacao:
                    for word in re.split("\se\s", bairro):
                        bairro_id = busca_bairro(cidade_id, word.lower())
                        salva_rodizio(data_inicio, data_fim, cidade_id, bairro_id, area_id)
                else:
                    bairro_id = busca_bairro(cidade_id, bairro.lower())
                    salva_rodizio(data_inicio, data_fim, cidade_id, bairro_id, area_id)

    logging.info(f"{today} - DADOS CARREGADOS COM SUCESSO.")


if __name__ == "__main__":
    start = time.time()
    main()
    logging.info(f"Tempo total: " + str(round(time.time() - start)) + " segundos")
