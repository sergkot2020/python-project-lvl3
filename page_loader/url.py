import os
from urllib.parse import urlparse

CHAR = '-'


def _replace_character(string: str):
    clear_string = string.strip('/')
    skip_symbols = ''.join(
        filter(lambda s: not (s.isalpha() or s.isnumeric()), clear_string)
    )
    replace_rule = str.maketrans(skip_symbols, CHAR * len(skip_symbols))
    return clear_string.translate(replace_rule)


def gen_page_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.netloc + parsed_url.path
    return f'{_replace_character(path)}.html'


def gen_dir_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.netloc + parsed_url.path
    return f'{_replace_character(path)}_files'


def gen_file_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.netloc + parsed_url.path
    name, tail = os.path.splitext(path)
    if not tail:
        tail = '.html'
    return f'{_replace_character(name)}{tail}'
