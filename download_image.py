import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup


def get_image_url(soup):
    image_tag = soup.find('div', class_='bookimage').find('img')
    return image_tag['src']


def fetch_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def download_image(title_url, book_title, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(book_title, 'lxml')
    image_url = urljoin(title_url, get_image_url(soup))
    image = fetch_image(image_url)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(image)
    return filepath