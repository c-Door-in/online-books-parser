import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests


def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def download_image(title_url, image_url, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = urljoin(title_url, image_url)
    image = fetch_image(url)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(image)
    return filepath