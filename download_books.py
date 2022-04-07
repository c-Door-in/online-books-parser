import logging
import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from pathvalidate import sanitize_filename

from parse_book_page import parse_book_page


module_logger = logging.getLogger('log.download_books')

def get_txt_filepath(folder, title, id):
    filename = sanitize_filename(f'{id}. {title}.txt')
    return os.path.join(folder, filename)


def download_txt(title_url, txt_url, id, title, folder='books/'):
    url = urljoin(title_url, txt_url)
    module_logger.debug(url)
    response = requests.get(url)
    response.raise_for_status()

    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = get_txt_filepath(folder, title, id)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
    return filepath


def download_image(title_url, image_url, folder='images/'):
    url = urljoin(title_url, image_url)
    module_logger.debug(url)
    response = requests.get(url)
    response.raise_for_status()

    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_book(book_id, title_page_url):
    response = requests.get(title_page_url)
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError
    module_logger.info(f'{book_id} {title_page_url}')
    parsed_page = parse_book_page(response.text)

    title = parsed_page['title']
    txt_url = parsed_page['txt_url']
    image_url = parsed_page['image_url']
    if not txt_url:
        return
    download_txt(title_page_url, txt_url, book_id, title)
    download_image(title_page_url, image_url)
    return parsed_page


def download_books(title_page_urls):
    books_summary = []
    for book_id, page_url in enumerate(title_page_urls, 1):
        try:
            parsed_page = download_book(book_id, page_url)
            if parsed_page:
                books_summary.append(parsed_page)
        except requests.HTTPError:
            continue
    return books_summary
