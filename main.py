import requests
import time
import random
import csv
from scrap_links import scrap_google_shopping
from scrap_wts import process_urls

def main():

    # Chama a função de scraping do Google Shopping
    scrap_google_shopping()

    print(f"Coleta de links finalizada, iniciando coleta de telefones...")

    #iniciar coleta de telefones
    process_urls()

if __name__ == "__main__":
    main()
