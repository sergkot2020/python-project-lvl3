from page_loader import download, get_file_name
import os
import tempfile

FILE_NAME = 'ru-hexlet-io-courses.html'
URL = 'https://ru.hexlet.io/courses'


def get_file(*args):
    path = os.path.join(*args)
    with open(path) as file:
        return file.read()


def test_converting_url_to_file_name():
    assert get_file_name(URL) == FILE_NAME


def test_load_page_to_tmp():
    with tempfile.TemporaryDirectory() as tmp_dir:
        download(URL, tmp_dir)
        file_name = get_file_name(URL)
        assert os.path.isfile(os.path.join(tmp_dir, file_name))

        correct_file = get_file('tests', 'fixtures', file_name)
        download_file = get_file(tmp_dir, file_name)

        assert len(correct_file) == len(download_file)
