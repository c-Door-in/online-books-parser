import argparse
import json
import os
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

import requests
import urllib3
from pathvalidate import sanitize_filename

from parse_book_page import parse_book_page
from parse_tululu_category import parse_tululu_category


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog='TULULU PARSER',
        description='Parser for online-library tululu.org',
    )
    parser.add_argument(
        '-from',
        '--start_id',
        default=1,
        help='Set start book ID for parsing range',
        type=int,
    )
    parser.add_argument(
        '-to',
        '--end_id',
        default=10,
        help='Set end book ID for parsing range',
        type=int,
    )
    return parser


def get_txt_filepath(folder, title, id):
    filename = sanitize_filename(f'{id}. {title}.txt')
    return os.path.join(folder, filename)


def download_txt(title_url, txt_url, id, title, folder='books/'):
    url = urljoin(title_url, txt_url)
    response = requests.get(url)
    response.raise_for_status()

    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = get_txt_filepath(folder, title, id)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(response.text)
    return filepath


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


def download_book(book_id, title_page_url):
    response = requests.get(title_page_url)
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError
    parsed_page = parse_book_page(response.text)

    title = parsed_page['title']
    txt_url = parsed_page['txt_url']
    image_url = parsed_page['image_url']
    if not txt_url:
        return
    download_txt(title_page_url, txt_url, book_id, title)
    download_image(title_page_url, image_url)
    return parsed_page


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = create_arg_parser()
    args = parser.parse_args()

    try:
        start_id, end_id = args.start_id, args.end_id
        if start_id > end_id:
            raise Exception('Start ID must be less than end ID')
    except Exception:
        raise

    category_url = 'https://tululu.org/l55/'
    categories_pages_count = 4
    title_page_urls = parse_tululu_category(category_url, categories_pages_count)

    print(f'parsing from {start_id} to {end_id}')
    books_summary = []
    for book_id, page_url in enumerate(title_page_urls[start_id:end_id+1], 1):
        try:
            parsed_page = download_book(book_id, page_url)
            if parsed_page:
                books_summary.append(parsed_page)
        except requests.HTTPError:
            continue
    
    with open('books.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_summary, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()