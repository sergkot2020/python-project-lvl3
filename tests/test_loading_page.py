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

BASE_PATH = os.path.join(os.getcwd(), TEST_DIR,  FIXTURE_DIR)

NOT_EXIST_PATH = '/some/not_exist/path'
NOT_EXIST_URL = 'https://not_exist_url.with_not_exist_domen'

CHECKING_HTML = 'processed.html'

ORIGIN_HTML = (
    'http://test_url.ru',
    gen_page_name('http://test_url.ru'),
    os.path.join(BASE_PATH, 'index.html')
)

FILES = [
    (
        'http://test_url.ru/images/test.jpg',
        gen_file_name('http://test_url.ru/images/test.jpg'),
        os.path.join(BASE_PATH, STATIC_DIR, '187.jpg')
    ),
    (
        'http://test_url.ru/static/css.css',
        gen_file_name('http://test_url.ru/static/css.css'),
        os.path.join(BASE_PATH, STATIC_DIR, 'style.css')
    ),
    (
        'http://test_url.ru/js/test.js',
        gen_file_name('http://test_url.ru/js/test.js'),
        os.path.join(BASE_PATH, STATIC_DIR, 'test.js')
    )
]


def read_file(path, mode='rb'):
    with open(path, mode) as file:
        return file.read()


def mock_files(mocker):
    files = []
    for file_data in FILES:
        url, file_name, path = file_data
        file = read_file(path)
        files.append((file_name, file))
        mocker.get(url, content=file)

    return files


def test_load_page():
    with requests_mock.Mocker() as mocker:
        main_url, page_name, path = ORIGIN_HTML
        origin_html = read_file(path, mode='r')
        mocker.get(main_url, text=origin_html)

        files = mock_files(mocker)

        checking_html = read_file(os.path.join(BASE_PATH, CHECKING_HTML), mode='r')
        with tempfile.TemporaryDirectory() as tmp_dir:
            download(main_url, path=tmp_dir)

            file_dir = gen_dir_name(URL)
            assert os.path.exists(os.path.join(tmp_dir, file_dir))

            for file_name, file in files:
                file_path = os.path.join(tmp_dir, file_dir, file_name)
                assert os.path.exists(file_path)
                assert read_file(file_path) == file

            path = os.path.join(tmp_dir, page_name)
            processed_html = read_file(path, mode='r')
            assert checking_html == processed_html


def test_os_error():
    with requests_mock.Mocker() as mocker:
        main_url, page_name, path = ORIGIN_HTML
        origin_html = read_file(path, mode='r')
        mocker.get(main_url, text=origin_html)

        mock_files(mocker)

        with pytest.raises(FileNotFoundError):
            download(main_url, path=NOT_EXIST_PATH)
            assert True

        with tempfile.TemporaryDirectory() as tmp_dir:
            download(main_url, path=tmp_dir)
            with pytest.raises(FileExistsError):
                download(main_url, path=tmp_dir)
                assert True


def test_network_error():
    with requests_mock.Mocker() as req_mocker:
        req_mocker.get(NOT_EXIST_URL, exc=requests.exceptions.ConnectionError)
        with pytest.raises(requests.exceptions.ConnectionError):
            with tempfile.TemporaryDirectory() as tmp_dir:
                download(NOT_EXIST_URL, path=tmp_dir)
                assert True

