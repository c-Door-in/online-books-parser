import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests


def download_image(title_url, image_url, folder='images/'):
    url = urljoin(title_url, image_url)
    response = requests.get(url)
    response.raise_for_status()

    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath