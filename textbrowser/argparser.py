from argparse import ArgumentParser

BrowserArgParser = ArgumentParser(description='Simple browser that dispays web pages')

BrowserArgParser.add_argument(
    '-cache-dir', 
    dest='dir',
    type=str, 
    default='./.cache', 
    help='Destination of webpages to be cached'
)

BrowserArgParser.add_argument(
    '-cache-size',
    dest='cache_size',
    type=int, 
    default=20, 
    help='Ammount of pages to be saved into cache directory'
)