import os
from typing import List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from page_loader.logger import get_logger
from page_loader.url import gen_dir_name, gen_file_name, gen_page_name
from progress.bar import Bar

logger = get_logger(__name__)


def download_assets(url, tags: list) -> List[tuple]:
    mapper = {
        'img': 'src',
        'link': 'href',
        'script': 'src',
    }
    page_netloc = urlparse(url).netloc

    assets = []
    bar = Bar(
        f'{"Downloading static files": <30}',
        fill='#',
        max=len(tags),
        check_tty=False
    )
    for tag in tags:
        bar.next()
        source = mapper[tag.name]
        link = tag.get(source)
        link_netloc = urlparse(link).netloc
        if link_netloc and link_netloc != page_netloc:
            continue
        file_url = urljoin(url, link)
        file_name = gen_file_name(file_url)
        request = requests.get(file_url)
        assets.append((tag, source, file_name, request))
    bar.finish()
    return assets


def save_content(request, file_name, path):
    bar = Bar(
        f'{file_name: <30}',
        fill='=',
        max=len(request.content) / 128,
        check_tty=False
    )
    with open(path, 'wb') as file:
        for chunk in request.iter_content(chunk_size=128):
            file.write(chunk)
            bar.next()
    bar.finish()


def download(url, path=os.getcwd()):
    req = requests.get(url)
    req.raise_for_status()
    logger.info(f'Get page from {url}')

    soup = BeautifulSoup(req.text, 'html.parser')

    images = soup.find_all('img')
    links = soup.find_all('link')
    scripts = soup.find_all('script')

    tags = [*images, *links, *scripts]
    if tags:
        assets = download_assets(url, tags)
        dir_name = gen_dir_name(url)
        dir_path = os.path.join(path, dir_name)

        logger.info(f'Create directory {dir_path}')
        os.mkdir(dir_path)

        for tag, source, file_name, request in assets:
            tag[source] = os.path.join(dir_name, file_name)
            save_content(
                request,
                file_name,
                os.path.join(dir_path, file_name)
            )

    page_name = gen_page_name(url)
    full_path = os.path.join(path, page_name)

    with open(full_path, "w") as file:
        file.write(str(soup.prettify(formatter='html5')))

    logger.info(f'Page {page_name} was saved to {full_path}')

    return full_path
