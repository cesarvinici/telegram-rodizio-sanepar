from bs4 import BeautifulSoup
import requests
import pandas as pd
from importlib import import_module
import sys
import os
from conf.settings import BASE_API_URL


"""
    Classe destinada a fazer o scrapping e retornar uma lista de objetos 
    contendo as informações necessárias
"""

class Scraping:
    RODIZIO_SITE = BASE_API_URL

    def get_scrapy(self):
        return self._get_data()

    def _connect(self):
        req = requests.get(self.RODIZIO_SITE)

        if req.status_code != 200:
            raise Exception("Something went wrong when connecting to the website!")

        return req.content

    def _get_data(self):
        content = self._connect()
        soup = BeautifulSoup(content, "html.parser")
        rodizio_lista = []
        for table in soup.find_all('table', attrs={"class": "views-table cols-5"}):
            tbody = table.findChild("tbody")

            for tr in tbody.find_all("tr"):
                td = tbody.findChild("td", attrs={"class": "views-field-field-grupo-rdz-data-value-1"})
                start = td.findChild("p").find("span", attrs={"class": "data-rodizio"}).text
                td = tbody.findChild("td", attrs={"class": "views-field views-field-field-grupo-rdz-data-value2"})
                end = td.findChild("p").find("span", attrs={"class": "data-rodizio"}).text
                td_lista = tr.findChild("td", attrs={"class": "views-field views-field-body"})

                for p in td_lista.find_all("p"):

                    if p.find("em"):
                        st = p.find_all("strong")
                        ema = p.find_all('em')
                        i = 0
                        while i < len(ema):
                            dados = {}
                            if len(ema) <= i and st[i].strong:
                                dados['cidade'] = st[i].text

                            else:
                                try:
                                    dados['cidade'] = st[i].text
                                except:
                                    i += 1
                                    continue
                            dados["inicio"] = start
                            dados["fim"] = end
                            dados['area'] = ema[i].text.replace(")", "").replace("(", "")
                            dados['bairros'] = ema[i].next_sibling.replace(":", "").strip().split(",")

                            rodizio_lista.append(dados)
                            i += 1
                    elif p.strong.strong:
                        dados = {"inicio": start, "fim": end, 'bairros': p.text.split(":")[1].split(","),
                                 'cidade': p.strong.text.replace(":", "").strip()}
                        rodizio_lista.append(dados)

        return rodizio_lista
