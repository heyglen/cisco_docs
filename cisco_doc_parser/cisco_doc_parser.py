from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from cisco_doc_parser.locations import location


class Docs:

    @classmethod
    def download(cls):
        index_url = location.index.nxos
        url = urlparse(index_url)
        base_url = f'{url.scheme}://{url.netloc}'

        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find(id='bookToc').find_all('a')
        links = [l.attrs.get('href') for l in links if l.string.endswith('Commands')]
        for link in links:
            link_url = f'{base_url}{link}'
            print(link_url)
