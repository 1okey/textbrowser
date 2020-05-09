from textbrowser.browser import TextBrowser
from textbrowser.config import BrowserConfig
from textbrowser.main import BrowserArgParser
from textbrowser.utils import InvalidQueryException

import pytest

@pytest.fixture
def browser():
    args = BrowserArgParser.parse_args()
    return TextBrowser(BrowserConfig(args))


@pytest.fixture
def config():
    args = BrowserArgParser.parse_args()
    return BrowserConfig(args)

    

VALID_DOMAINS = [
    ('https://google.com', ('https://', 'google', 'com')),
    ('google.com', ('https://', 'google', 'com')),
    ('python.org', ('https://', 'python', 'org')),
]

INVALID_DOMAINS = [
    'https://google',
    'google'
    'https://+-=_.com'
]

def test_valid_domains(browser):
    # mock class
    for domain, expected in VALID_DOMAINS:
        assert expected == tuple(browser.parse_query(domain))

def test_invalid_domains(browser):
    # mock class
    for domain in INVALID_DOMAINS:
        with pytest.raises(InvalidQueryException):
            browser.parse_query(domain)


def test_config(config):
    assert config.cache_dir == './.cache'
    assert config.cache_size == 20


def test_requests(browser):
    pass
    # TODO
