import logging
import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
from pathvalidate import sanitize_filename

from parse_book_page import parse_book_page


module_logger = logging.getLogger('log.download_books')

def download_txt(title_url, txt_url, book_id, title, dest_folder):
    url = urljoin(title_url, txt_url)
    module_logger.debug(url)
    response = requests.get(url)
    response.raise_for_status()

    folder = f'{dest_folder}/books/'
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(f'{book_id}-я книга. {title}.txt')
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
    return filepath


def download_image(title_url, image_url, dest_folder):
    url = urljoin(title_url, image_url)
    module_logger.debug(url)
    response = requests.get(url)
    response.raise_for_status()

    folder = f'{dest_folder}/images/'
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_book(book_id, title_page_url, dest_folder, skip_imgs, skip_txt):
    response = requests.get(title_page_url)
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError
    parsed_page = parse_book_page(response.text)
    if not parsed_page['txt_url']:
        return
    txtpath = download_txt(title_page_url,
                            parsed_page['txt_url'],
                            book_id,
                            parsed_page['title'],
                            dest_folder) if not skip_txt else None
    imagepath = download_image(title_page_url,
                               parsed_page['image_url'],
                               dest_folder) if not skip_imgs else None
    return {
        'title': parsed_page['title'],
        'author': parsed_page['author'],
        'txtpath': txtpath,
        'imagepath': imagepath,
        'genres': parsed_page['genres'],
        'comments': parsed_page['comments'],
    }


def download_books(title_page_urls, dest_folder, skip_imgs, skip_txt):
    books_summary = []
    for book_id, page_url in enumerate(title_page_urls, 1):
        module_logger.info(f'{book_id} {page_url}')
        try:
            download_result = download_book(
                book_id,
                page_url,
                dest_folder,
                skip_imgs,
                skip_txt,
            )
            if download_result:
                books_summary.append(download_result)
        except requests.HTTPError:
            continue
    return books_summary
