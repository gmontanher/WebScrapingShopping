import requests
from bs4 import BeautifulSoup
import time
import random
import csv
from urllib.parse import urlparse, urlunparse


def scrap_google_shopping():
    # Definindo o termo de pesquisa e a URL base para pesquisa no Google Shopping
    termo_pesquisa = "pulseiras e colares"
    url_base = f"https://www.google.com/search?q={termo_pesquisa}&tbm=shop&start="

    # Inicializando uma variável para contar a quantidade de páginas puxadas
    quantidade_paginas_puxadas = 0

    # Nome do arquivo CSV onde os domínios serão armazenados
    nome_arquivo_csv = "links.csv"

    # Definindo o número máximo de páginas a serem percorridas
    maximo_paginas = 1000
    paginas_por_consulta = 40
    consultas_por_intervalo = 40  # Novo: Definindo a quantidade de consultas por intervalo

    # Lista de palavras-chave a serem filtradas
    palavras_chave = ["shein", "mercadolivre", "magazineluiza", "kabum", "submarino", "extra", "casasbahia", "renner", "shopee", "google", "cea", "pontofrio", "riachuelo", "centauro", "decathlon", "carrefour", "amazon", "ebay", "mercadolivre", "americanas", "submarino", "shopee", "magazineluiza", "olx", "netshoes", "dafiti", "zoom", "centauro", "casasbahia", "extra", "pontofrio", "carrefour", "walmart", "leroymerlin", "zattini", "mercadoshops", "elo7", "kabum", "madeiramadeira", "etna", "cea", "lojasrenner", "enjoei", "tricae", "girafa", "petlove", "casasbahiamarketplace", "pernambucanas", "fastshop", "mercadopago", "melhorenvio", "colombo", "b2wmarketplace", "bebestore", "drogasil", "maquinadevendas", "onofreeletro", "todaoferta.uol", "saraiva", "ciadoslivros", "fnac", "havan", "shoptime", "ricardoeletro", "gazinmarketplace", "centauromarketplace", "olist", "vivaramarketplace", "paguemenos", "bebe", "bebemamao", "globoplay.globo", "puket", "dinda", "posthaus", "lojasmorenarosa", "gpa"]

    # Lista para armazenar os links encontrados
    links_encontrados = []


    # Loop geral para realizar consultas até atingir o número máximo de páginas
    while quantidade_paginas_puxadas < maximo_paginas:
        # Inicializando uma variável para contar a quantidade de páginas puxadas na consulta atual
        paginas_na_consulta_atual = 0

        # Loop através das páginas de resultados da pesquisa
        while paginas_na_consulta_atual < paginas_por_consulta:
            # Construindo a URL da página atual
            url = url_base + str(quantidade_paginas_puxadas + 1)

            # Fazendo uma solicitação HTTP para obter o conteúdo da página
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
            response = requests.get(url, headers=headers)

            # Verificando se a solicitação foi bem-sucedida (status_code 200)
            if response.status_code == 200:
                # Analisando o conteúdo HTML da página usando BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Encontrando todos os links na página
                links_pagina = soup.find_all('a')

                # Adicionando os links da página atual à lista de links encontrados
                for link in links_pagina:
                    href = link.get('href')
                    if href:
                        links_encontrados.append(href)

                # Incrementando a quantidade de páginas puxadas na consulta atual
                paginas_na_consulta_atual += 1

                # Incrementando a quantidade total de páginas puxadas
                quantidade_paginas_puxadas += 1

                # Exibindo a URL atual
                print("URL:", url)

                # Tempo variável entre 0.3 e 1.5 segundos
                tempo_espera = random.uniform(50, 65)
                time.sleep(tempo_espera)

            else:
                print(f"Falha ao acessar a página {quantidade_paginas_puxadas + 1}")

        # Limpando os links e coletando apenas os endereços principais
        links_finais = [link for link in links_encontrados if '/url?q=' in link]
        links_finais_sem_q = [link.replace("/url?q=", "") for link in links_finais]

        # Filtrando os links removendo os que contêm palavras-chave
        links_finais_filtrados = [link for link in links_finais_sem_q if not any(palavra in link for palavra in palavras_chave)]

        # Extraindo apenas os endereços principais (domínios) dos links filtrados
        dominios = []
        for link in links_finais_filtrados:
            parsed_url = urlparse(link)
            dominio = urlunparse((parsed_url.scheme, parsed_url.netloc, '', '', '', ''))
            dominios.append(dominio)

        # Removendo duplicatas mantendo a ordem
        dominios_unicos = list(dict.fromkeys(dominios))

        # Escrevendo os domínios em um arquivo CSV
        with open(nome_arquivo_csv, 'a', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            for dominio in dominios_unicos:
                writer.writerow([dominio])

        # Limpeza da lista de links para a próxima iteração
        links_encontrados.clear()

        # Verificando se é necessário aplicar o intervalo de 1 minuto
        if quantidade_paginas_puxadas % consultas_por_intervalo == 0 and quantidade_paginas_puxadas > 0:
            print(f"Intervalo de 1 minuto antes da próxima consulta (Total de páginas puxadas: {quantidade_paginas_puxadas})")
            time.sleep(80)  # Aguarda 1 minuto antes da próxima consulta

    # No final do seu código, você pode exibir ou usar a variável `quantidade_paginas_puxadas` conforme necessário
    print(f"Todas as consultas foram concluídas. Total de páginas puxadas: {quantidade_paginas_puxadas}")

    return
