import requests
from bs4 import BeautifulSoup
import re
import csv

def extract_phone_numbers(url):
    try:
        # Enviar uma solicitação HTTP para obter o conteúdo da página
        response = requests.get(url)
        response.raise_for_status()  # Verificar se há erros na solicitação
        content = response.content

        # Parse do HTML com BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Encontrar elementos no footer que podem conter números de telefone
        footer_elements = soup.find_all(['footer', 'div', 'span', 'p', 'a'])

        # Lista para armazenar números de telefone encontrados
        phone_numbers = []

        # Expressão regular mais flexível para encontrar números de telefone
        phone_regex = re.compile(r'(?:(?:\+|00)\d{1,3})?[ -]?\(?0?\d{1,3}\)?[ -]?\d{4,5}[ -]?\d{4}')

        for element in footer_elements:
            # Extrair texto do elemento
            element_text = element.get_text()

            # Encontrar números de telefone usando a expressão regular
            matches = phone_regex.findall(element_text)

            # Adicionar números de telefone à lista
            phone_numbers.extend(matches)

        # Remover duplicatas usando um conjunto (set)
        unique_phone_numbers = list(set(phone_numbers))

        return unique_phone_numbers
    except Exception as e:
        print(f"Erro ao processar a URL {url}: {str(e)}")
        return []

def process_urls(input_csv='links.csv', output_csv='links_numeros.csv'):
    with open(input_csv, 'r', encoding='utf-8') as input_file, open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Escrever cabeçalho no arquivo de saída
        csv_writer.writerow(['URL', 'Phone Numbers'])

        # Pular a primeira linha (cabeçalho) do arquivo de entrada
        next(csv_reader, None)

        # Processar cada linha do CSV
        for row in csv_reader:
            url = row[0]  # Assumindo que a URL está na primeira coluna do arquivo CSV

            # Extrair números de telefone
            phone_numbers = extract_phone_numbers(url)

            # Escrever a URL e os números de telefone no arquivo de saída
            csv_writer.writerow([url, ', '.join(phone_numbers)])

            # Exibir os números de telefone únicos encontrados para cada URL
            print(f"{url}: {phone_numbers}")
