from loguru import logger
from os import mkdir, path
from sys import stderr, stdin
from os import remove, listdir


class BrowserCache:

    FILE_FORMAT = 'txt'

    def __init__(self, arguments):
        logger.add(stderr, format="{time} {level} {message}", filter="TextBrowser", level="INFO")

        self.cache_dir = arguments.dir

        if not path.exists(self.cache_dir):
            mkdir(self.cache_dir)

        self.cache_size = arguments.cache_size
        self.queue = []

    def set_cache_size(self, new_size):
        if new_size > self.cache_size:
            self.cache_size = new_size 

    def clear(self):
        logger.debug('User cleared browser cache')

        for file in listdir(self.cache_dir):
            remove(f'{self.cache_dir}/{file}')

    def save(self, file_name, content):
        if self.cache_size == len(self.queue):
            logger.debug(f'Reached size capacity, removing oldest file')
            oldest_file = self.queue.pop(0)
            self.remove(oldest_file)

        file_path = f'{self.cache_dir}/{file_name}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        self.queue.append(file_name)
        logger.debug(f'Space left for {self.cache_size - len(self.queue)} sites')


    def get_cached_site(self, file_name):
        logger.debug(f'Loading from cache')

        file_path = f'{self.cache_dir}/{file_name}.txt'
        with open(file_path, 'r', encoding='utf-8') as cached_site:
            print(*cached_site.readlines())

    def remove(self, file_name):
        remove(f'{self.cache_dir}/{file_name}.txt')

    def has(self, file_name):
        logger.debug(f'Found in cache')

        return path.exists(f'{self.cache_dir}/{file_name}.txt')