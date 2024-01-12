import requests
from bs4 import BeautifulSoup
import time
import random
import csv
from urllib.parse import urlparse, urlunparse

max_links_desejados = 100


def scrap_google_shopping():
    termo_pesquisa = "móveis"
    url_base = f"https://www.google.com/search?q={termo_pesquisa}&tbm=shop&start="
    nome_arquivo_csv = "links.csv"
    consultas_por_intervalo = 40
    palavras_chave = [
    "shein", "mercadolivre", "magazineluiza", "kabum", "submarino", "extra", 
    "casasbahia", "renner", "shopee", "google", "cea", "pontofrio", "riachuelo", 
    "centauro", "decathlon", "carrefour", "amazon", "ebay", "mercadolivre",
    "americanas", "submarino", "shopee", "magazineluiza", "olx", "netshoes", 
    "dafiti", "zoom", "centauro", "casasbahia", "extra", "pontofrio", "carrefour", 
    "walmart", "leroymerlin", "zattini", "mercadoshops", "elo7", "kabum", 
    "madeiramadeira", "etna", "cea", "lojasrenner", "enjoei", "tricae", "girafa", 
    "petlove", "casasbahiamarketplace", "pernambucanas", "fastshop", "mercadopago", 
    "melhorenvio", "colombo", "b2wmarketplace", "bebestore", "drogasil", 
    "maquinadevendas", "onofreeletro", "todaoferta.uol", "saraiva", "ciadoslivros", 
    "fnac", "havan", "shoptime", "ricardoeletro", "gazinmarketplace", 
    "centauromarketplace", "olist", "vivaramarketplace", "paguemenos", "bebe", 
    "bebemamao", "globoplay.globo", "puket", "dinda", "posthaus", 'camicado', 'mobly', 
    "lojasmorenarosa", "gpa"
]

    quantidade_links_coletados = 0
    quantidade_paginas_puxadas = 0
    max_links_desejados = 3


    def extrair_dominio(link):
        return urlunparse(urlparse(link)[:2] + ('',) * 4)

    def ler_csv():
        try:
            with open(nome_arquivo_csv, 'r', encoding='utf-8') as arquivo_csv:
                reader = csv.reader(arquivo_csv)
                return set(row[0] for row in reader)
        except FileNotFoundError:
            return set()

    def escrever_csv(dominios_unicos):
        with open(nome_arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerows([[dominio] for dominio in dominios_unicos])

    links_existentes = ler_csv()

    while quantidade_links_coletados < max_links_desejados:
        url = url_base + str(quantidade_paginas_puxadas + 1)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links_pagina = [link.get('href') for link in soup.find_all('a') if link.get('href')]

            links_encontrados = [link.replace("/url?q=", "") for link in links_pagina if '/url?q=' in link]
            links_filtrados = [link for link in links_encontrados if not any(palavra in link for palavra in palavras_chave)]
            dominios_unicos = set(map(extrair_dominio, links_filtrados))

            links_novos = dominios_unicos - links_existentes

            # if not links_novos:
            #     print(f"Nenhum link novo encontrado. Encerrando o programa.")
            #     break

            escrever_csv(links_novos)
            links_existentes.update(links_novos)
            quantidade_links_coletados += len(links_novos)

            quantidade_paginas_puxadas += 1

            print("URL:", url)
            print(f"Total de links coletados: {quantidade_links_coletados}")

            time.sleep(random.uniform(15, 20))

            if quantidade_paginas_puxadas % consultas_por_intervalo == 0 and quantidade_paginas_puxadas > 0:
                print(f"Intervalo de 15 segundos antes da próxima consulta")
                time.sleep(15)

        else:
            print(f"Falha ao acessar a página {quantidade_paginas_puxadas + 1}")
            break