import loguru
from os import mkdir, path


class BrowserConfig:
    def __init__(self, arguments):
        self.cache_dir = arguments.dir

        if not path.exists(self.cache_dir):
            mkdir(self.cache_dir)

        self.cache_size = arguments.cache_size