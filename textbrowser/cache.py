import loguru
from os import mkdir, path


class BrowserCache:
    def __init__(self, arguments):
        self.cache_dir = arguments.dir

        if not path.exists(self.cache_dir):
            mkdir(self.cache_dir)

        self.cache_size = arguments.cache_size

    def set_cache_size(self, new_size):
        if new_size > self.cache_size:
            self.cache_size = new_size 

    def clear(self):
        pass

    def cache_site(self):
        pass

    def get_cached_site(self):
        pass