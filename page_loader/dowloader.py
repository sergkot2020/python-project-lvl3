import requests
import os

format_symbol = str.maketrans('./', '--')


def get_file_name(url):
    url_tail = url.split('//')[-1]
    file_name = f'{url_tail.translate(format_symbol).strip()}.html'
    return file_name


def download(url, path):
    """
    https://ru.hexlet.io/courses
    ru-hexlet-io-courses.html

    """
    r = requests.get('https://ru.hexlet.io/courses', stream=True)
    file_name = get_file_name(url)
    full_path = os.path.join(path, file_name)

    with open(full_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


if __name__ == '__main__':
    download(
        'https://ru.hexlet.io/courses',
        '/home/serg/PycharmProjects/python-project-lvl3'
    )
