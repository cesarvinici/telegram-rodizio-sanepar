from sqlalchemy import create_engine
import datetime
import os
import pandas as pd


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, "sanepar.db")

def db_connect():
    """
    Conectando no banco de dados
    """
    return create_engine("sqlite:///" + DB_PATH)


def get_cidades():
    conn = db_connect()
    query = "SELECT cidade from cidades;"
    return pd.read_sql(query, conn)

def get_bairros(cidade):
    conn = db_connect()
    query = f"SELECT bairro from bairros as b join cidades c on c.id = b.cidade_id where c.cidade = '{cidade.strip().lower()}' order by bairro asc;"
    return pd.read_sql(query, conn)

def get_sql_cidade():
    with open("src/model/busca_rodizio_cidade.sql", 'r') as file_open:
        result = file_open.read()
    return result

def get_sql_bairro():
    with open("src/model/busca_rodizio_bairro.sql", 'r') as file_open:
        result = file_open.read()
    return result

def busca_rodizio(cidade, bairro = None):
    conn = db_connect()
    dt_inicio = datetime.date.today().strftime("%Y-%m-%d")
    if(bairro):
        sql = get_sql_bairro()
        result = pd.read_sql(sql.format(cidade=cidade.lower(), bairro=bairro.lower(), dt_inicio = dt_inicio), conn)
    else:
        sql = get_sql_cidade()
        result = pd.read_sql(sql.format(cidade=cidade.lower(), dt_inicio = dt_inicio), conn)
    
    return rodizio_string(result, cidade.title())

def rodizio_string(rodizio, cidade):
    msg = f"*{cidade}*:"
    for date in list(rodizio['data_inicio'].unique()):
        data = rodizio[rodizio['data_inicio'] == date]
        inicio = datetime.datetime.strptime(date, "%Y-%m-%d %I:%M").strftime("%d/%m/%Y às %I:%M")
        fim = datetime.datetime.strptime(data.iloc[0].data_fim, "%Y-%m-%d %I:%M").strftime("%d/%m/%Y às %I:%M")
        msg += f"\n\tInicio: {inicio} - Fim {fim}\n"
        for bairro in list(data['bairro'].unique()):
            msg += f"\t *{bairro.title()}*\n"
            bairros_data = data[data['bairro'] == bairro]
            for area in list(bairros_data['area'].unique()):
                msg += f"\t\t\tArea: {area}\n"
    return msg