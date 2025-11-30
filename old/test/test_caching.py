from textbrowser.cache import BrowserCache
from textbrowser.argparser import BrowserArgParser

import pytest

@pytest.fixture
def default_cache():
    args = BrowserArgParser.parse_args()
    return BrowserCache(args)

@pytest.fixture
def cache():
    args = BrowserArgParser.parse_args('-cache-dir .cache -cache-size 5'.split())
    return BrowserCache(args)

def test_defaulit_cache(default_cache):
    assert default_cache.cache_dir == './.cache'
    assert default_cache.cache_size == 10

def test_changes_size(default_cache):
    assert default_cache.cache_dir == './.cache'
    assert default_cache.cache_size == 10
    default_cache.set_cache_size(2)
    assert default_cache.cache_size == 2

def test_caches(cache):
    cache.clear()
    assert cache.is_empty()

    assert cache.cache_dir == '.cache'
    assert cache.cache_size == 5

    assert cache.has("google.com") == False
    cache.save("google.com", "content")
    assert cache.has("google.com") == True

    
def test_caches_and_removes(cache):
    cache.clear()
    assert cache.is_empty()

    file_name = "google.com"
    assert cache.has(file_name) == False
    cache.save(file_name, "content")
    assert cache.has(file_name) == True
    cache.remove(file_name)
    assert cache.has(file_name) == False

        
def test_removes_old(cache):
    cache.clear()
    assert cache.is_empty()

    for i in range(0, 6):
        cache.save(str(i), str(i) + " content")

    assert len(cache.queue) == 5
    assert cache.has(0) == False

def test_clears_cache(cache):
    cache.clear()
    assert cache.is_empty()

    for i in range(0, 6):
        cache.save(str(i), str(i) + " content")

    assert len(cache.queue) == 5
    cache.clear()
    assert len(cache.queue) == 0









