import requests
import os
from pathlib import Path
from urllib.parse import urljoin

from pathvalidate import sanitize_filename


def get_filepath(folder, title, id):
    filename = sanitize_filename(f'{id}. {title}.txt')
    return os.path.join(folder, filename)


def download_txt(title_url, txt_url, id, title, folder='books/'):
    url = urljoin(title_url, txt_url)
    response = requests.get(url)
    response.raise_for_status()

    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = get_filepath(folder, title, id)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath