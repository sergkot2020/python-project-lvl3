import os
import tempfile

import pytest
import requests
import requests_mock
from page_loader import download
from page_loader.dowloader import gen_dir_name, gen_file_name, gen_page_name

URL = 'http://test_url.ru'

TEST_DIR = 'tests'
STATIC_DIR = 'static'
FIXTURE_DIR = 'fixtures'

BASE_PATH = os.path.join(os.getcwd(), TEST_DIR, FIXTURE_DIR)
NOT_EXIST_PATH = os.path.join('some', 'doesn`t exist', 'path')
NOT_EXIST_URL = 'https://not_exist_url.with_not_exist_domen'

CHECKING_HTML = 'processed.html'
ORIGIN_HTML = (
    'http://test_url.ru',
    'test-url-ru.html',
    os.path.join(BASE_PATH, 'index.html')
)
DIR_NAME = 'test-url-ru_files'
ASSETS = [
    (
        'http://test_url.ru/images/test.jpg',
        'test-url-ru-images-test.jpg',
        os.path.join(BASE_PATH, STATIC_DIR, '187.jpg')
    ),
    (
        'http://test_url.ru/static/css.css',
        'test-url-ru-static-css.css',
        os.path.join(BASE_PATH, STATIC_DIR, 'style.css')
    ),
    (
        'http://test_url.ru/js/test.js',
        'test-url-ru-js-test.js',
        os.path.join(BASE_PATH, STATIC_DIR, 'test.js')
    )
]


def read_file(path, mode='rb'):
    with open(path, mode) as file:
        return file.read()


def mock_assets(mocker):
    assets = []
    for url, file_name, path in ASSETS:
        file = read_file(path)
        assets.append((file_name, file))
        mocker.get(url, content=file)

    return assets


def test_load_page():
    with requests_mock.Mocker() as mocker:
        main_url, page_name, path = ORIGIN_HTML
        origin_html = read_file(path, mode='r')
        mocker.get(main_url, text=origin_html)

        assets = mock_assets(mocker)

        checking_html = read_file(os.path.join(BASE_PATH, CHECKING_HTML), mode='r')
        with tempfile.TemporaryDirectory() as tmp_dir:
            download(main_url, path=tmp_dir)

            assert os.path.exists(os.path.join(tmp_dir, DIR_NAME))

            for file_name, asset in assets:
                file_path = os.path.join(tmp_dir, DIR_NAME, file_name)
                assert os.path.exists(file_path)
                assert read_file(file_path) == asset

            path = os.path.join(tmp_dir, page_name)
            processed_html = read_file(path, mode='r')
            assert checking_html == processed_html


def test_os_error():
    with requests_mock.Mocker() as mocker:
        main_url, page_name, path = ORIGIN_HTML
        origin_html = read_file(path, mode='r')
        mocker.get(main_url, text=origin_html)

        mock_assets(mocker)

        with pytest.raises(FileNotFoundError):
            assert download(main_url, path=NOT_EXIST_PATH)


def test_network_error():
    with requests_mock.Mocker() as req_mocker:
        req_mocker.get(NOT_EXIST_URL, exc=requests.exceptions.ConnectionError)
        with pytest.raises(requests.exceptions.ConnectionError):
            with tempfile.TemporaryDirectory() as tmp_dir:
                download(NOT_EXIST_URL, path=tmp_dir)

        code_errors = [404, 500]
        for code in code_errors:
            req_mocker.get(NOT_EXIST_URL, status_code=code)
            with tempfile.TemporaryDirectory() as tmp_dir:
                with pytest.raises(requests.exceptions.HTTPError):
                    download(NOT_EXIST_URL, path=tmp_dir)
