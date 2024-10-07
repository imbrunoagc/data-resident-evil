import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from typing import Dict

from paramns import COOKIES, HEADERS

def get_content(url: str):
    response = requests.get(url=url, cookies=COOKIES, headers=HEADERS)
    print(response.status_code)
    return response

def get_basic_infos(soup):
    div_page = soup.find('div', class_ = 'td-page-content')
    paragrafo = div_page.find_all('p')[1]
    ems = paragrafo.find_all('em')
    data = dict()

    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        valor = valor.strip(" ")
        data[chave] = valor
    return data

def get_aparicoes(soup): 
    lis = (soup
        .find('div', class_ = 'td-page-content')
        .find('h4')
        .find_next()
        .find_all('li'))
    
    return [i.text for i in lis]

def get_personagem_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Não foi possivel obter os dados")
    else:
        soup = BeautifulSoup(resp.text)

        data = get_basic_infos(soup)
        data['aparicoes'] = get_aparicoes(soup)
        return data

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/'
    resp = requests.get(url=url, headers=HEADERS, cookies=COOKIES)
    soup_personagens = BeautifulSoup(resp.text) 
    ancoras = (soup_personagens.find('div', class_ = 'td-page-content')
                            .find_all('a'))

    links = [i["href"] for i in ancoras]
    return links

def run_collect_data():
    data = []
    urls_blocked = ['https://www.residentevildatabase.com/doug-re5-desperate-escape/']

    links = get_links()

    for i in tqdm(links):
        if i in urls_blocked:
            continue
        print(i)
        d = get_personagem_infos(i)
        d['link'] = i
        d['name'] = i.split('/')[-2]
        data.append(d)
    return data

def write_data_raw(data: Dict) -> None:
    with open(FILE_PATH, 'w') as output_file:
        try:
            json.dump(data, output_file, indent=2)
            print(f'success in writing the file: {FILE_PATH}')
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    FILE_PATH = '././data/raw/basic_information_characters.json'

    data = run_collect_data()
    if data:
        write_data_raw(data)
