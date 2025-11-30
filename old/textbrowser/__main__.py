from textbrowser.browser import TextBrowser
from textbrowser.cache import BrowserCache
from textbrowser.argparser import BrowserArgParser

args = BrowserArgParser.parse_args()
cache = BrowserCache(args)
browser = TextBrowser(cache)
browser.run()
