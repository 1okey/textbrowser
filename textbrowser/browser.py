from re import match
from os import path
from sys import stderr, stdin

from requests import get
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from colorama import init as colorama_init, Fore
from loguru import logger

from textbrowser.utils import InvalidQueryException, InvalidRequestError


class TextBrowser:
    TAGS = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    REGEX = r'(https?:\/\/)?([-0-9a-z.]+[.]?){1,2}\.([a-z]{2,3})'
    COMMANDS = ('back', 'clean', 'exit')

    def __init__(self, cache):
        logger.add(stderr, format="{time} {level} {message}", filter="TextBrowser", level="INFO")

        colorama_init()
        self.cache = cache
        self.queue = []

    def handle_command(self, command):
        if command == 'exit':
            logger.debug('User exits application')
            exit(0)
        elif command == 'back':
            if len(self.queue) > 0:
                query = self.queue.pop()
                if query in TextBrowser.COMMANDS:
                    self.handle_command(query)
                else:
                    self.handle_request(query)
            else:
                logger.debug('User requested last command from empty queue')
                print('Request queue is empty, skipping')
        elif command == 'clean':
            self.cache.clear()

    def handle_request(self, query):
        self.queue.append(query)
        query = self.queue[len(self.queue) - 1]

        try:
            protocol, name, domain = self.parse_query(query)
            self.get_site(protocol, name, domain)
        except InvalidQueryException as e:
            logger.debug(f'InvalidQueryException: {e.message}')
        except InvalidRequestError as e:
            logger.debug(f'InvalidRequestError: {e.message}')

    def parse_query(self, query):
        domain_match = match(TextBrowser.REGEX, query)
        protocol, name, domain = domain_match.groups() if domain_match else (None, None, None)
        
        protocol = protocol if protocol else 'https://'

        if name == None or domain == None:
            raise InvalidQueryException()

        return protocol, name, domain

    def scrape_response(self, response):
        logger.debug('Scrapping received response')
        soup = BeautifulSoup(response.content, 'html.parser')
        found_elems = soup.find_all(TextBrowser.TAGS, recursive=True)
        page_content = ''

        for el in found_elems:
            el_content = el.get_text().strip().replace('\n', ' ')
            if el.name.find('h') >= 0:
                el_content = Fore.CYAN + f'{el_content}\n\n'
            if el.name == 'p':
                el_content = Fore.LIGHTWHITE_EX + f'\n{el_content}\n'
            if el.name == 'a':
                el_content = Fore.BLUE + f'> {el_content}\n'

            page_content += f'{el_content} ' + Fore.RESET

        return page_content

    def get_site(self, protocol, name, domain):
        file_name = f'{name}.{domain}'
        logger.debug(f'Requesting {name}.{domain}')
        if self.cache.has(file_name):
            print(self.cache.get_cached_site(file_name))
        elif name and domain:
            logger.debug(f'Getting {name}.{domain}...')
            try:
                logger.debug(f'Starting scraping')
                site_content = self.scrape_response(get(f'{protocol}{name}.{domain}'))
                logger.debug(f'Saving file')
                
                self.cache.save(file_name, site_content)
                print(site_content)

            except ConnectionError:
                raise InvalidRequestError()
        else:
            print('Error: Incorrect URL')
            logger.debug(f'Failed requesting {name}.{domain}')

    def run(self):
        while True:
            query = input('Enter url you want to check out: ')
            logger.debug(f'User input: {query}')
            if query in TextBrowser.COMMANDS:
                self.handle_command(query)
            else:
                self.handle_request(query)

