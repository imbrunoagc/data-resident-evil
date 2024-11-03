import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from typing import Dict, List

class collect:
    def __init__(self, cookies, headers) -> None:
        self.cookies = cookies
        self.headers = headers

    def get_content(self, url: str) -> List:
        response = requests.get(url=url, cookies=self.cookies, headers=self.headers)
        print(response.status_code)
        return response

    def get_basic_infos(self, soup: List) -> Dict:
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

    def get_aparicoes(self, soup: List) -> List: 
        lis = (soup
            .find('div', class_ = 'td-page-content')
            .find('h4')
            .find_next()
            .find_all('li'))
        
        return [i.text for i in lis]

    def get_personagem_infos(self, url: str):
        resp = self.get_content(url)
        if resp.status_code != 200:
            print("Não foi possivel obter os dados")
        else:
            soup = BeautifulSoup(resp.text)

            data = self.get_basic_infos(soup)
            data['aparicoes'] = self.get_aparicoes(soup)
            return data

    def get_links(self) -> List:
        url = 'https://www.residentevildatabase.com/personagens/'
        resp = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        soup_personagens = BeautifulSoup(resp.text) 
        ancoras = (
                    soup_personagens
                    .find('div', class_ = 'td-page-content')
                    .find_all('a')
                    )

        links = [i["href"] for i in ancoras]
        return links

    def run_collect_data(self) -> List:
        data = []
        urls_blocked = ['https://www.residentevildatabase.com/doug-re5-desperate-escape/']

        links = self.get_links()

        for i in tqdm(links):
            if i in urls_blocked:
                continue
            print(i)
            d = self.get_personagem_infos(i)
            d['link'] = i
            d['name'] = i.split('/')[-2]
            data.append(d)
        return data

    def write_data_raw(self, data: Dict, file_path: str) -> None:
        with open(file_path, 'w') as output_file:
            try:
                json.dump(data, output_file, indent=2)
                print(f'success in writing the file: {FILE_PATH}')
            except Exception as e:
                print(f'Error: {e}')
    
    def run_collect(self, file_path: str = None, if_local: bool = True) -> None:
        data = self.run_collect_data()
        if data:
            if if_local:
                return self.write_data_raw(data, file_path)
            else:
                return data

if __name__ == "__main__":
    from paramns import COOKIES, HEADERS
    FILE_PATH = '././data/raw/basic_information_characters.json'
    data  = collect(COOKIES, HEADERS).run_collect(FILE_PATH, False)
    print(data)