import logging
from urllib.parse import urlparse

import requests
import bs4

from cisco_doc.locations import location
from cisco_doc.command.factory import CommandFactory
from cisco_doc.utilities.log_setup import log_setup

logger = log_setup('cisco_cmd')
logger.setLevel(logging.DEBUG)


class Docs:

    @classmethod
    def _pages(cls):
        index_url = location.index.nxos
        url = urlparse(index_url)
        base_url = f'{url.scheme}://{url.netloc}'

        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        links = soup.find(id='bookToc').find_all('a')
        links = [l.attrs.get('href') for l in links if l.string.endswith('Commands')]
        for link in links:
            url = f'{base_url}{link}'
            logger.debug(f'Downloading {url}')
            response = requests.get(url)
            yield bs4.BeautifulSoup(response.text, 'html.parser')

    @classmethod
    def _commands(cls):
        for page in cls._pages():
            sections = page.find(id='chapterContent')
            for section in sections.children:
                if not isinstance(section, bs4.element.Tag):
                    continue
                h2 = section.find('h2')
                if h2 and 'pCRC_CmdRefCommand' in h2['class']:
                    yield CommandFactory.build(section)

    @classmethod
    def download(cls):
        for cmd in cls._commands():
            import ipdb; ipdb.set_trace()