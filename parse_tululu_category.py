import argparse
import logging
import json
from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup

from download_books import download_books


logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
fmtdate = '%H:%M:%S'
formatter = logging.Formatter(fmtstr, fmtdate)

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog='TULULU PARSER',
        description='Parser for online-library tululu.org',
    )
    parser.add_argument(
        '-from',
        '--start_page',
        default=1,
        help='Set start page of the category list',
        type=int,
    )
    parser.add_argument(
        '-to',
        '--end_page',
        help='Set end page of the category list',
        type=int,
    )
    return parser


def is_final_page(soup, page_id):
    selector = '#content .npage'
    return str(page_id) not in [
        npage.text for npage in soup.select(selector)
    ]


def parse_book_urls(soup):
    card_tags = soup.select('.d_book')
    return [book_url.select_one('[href^="/b"]')['href'] for book_url in card_tags]


def parse_tululu_category(category_url, start_page_id, end_page_id):
    book_urls = list()
    page_id = start_page_id
    
    while True:
        logger.info(f'parsing page: {page_id}')
        list_page_url = f'{category_url}{page_id}/'
        response = requests.get(list_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for book_url in parse_book_urls(soup):
            book_urls.extend([urljoin(category_url, book_url)])
        page_id += 1
        if end_page_id:
            if page_id > end_page_id:
                break
        if is_final_page(soup, page_id):
            break
        
    return book_urls


def main():
    logger.info('Starting program')
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = create_arg_parser()
    args = parser.parse_args()
    
    start_page_id, end_page_id = args.start_page, args.end_page
    if end_page_id:
        try:
            if start_page_id > end_page_id:
                raise Exception('Start page number must be less than the end one')
        except Exception:
            raise
    
    category_url = 'https://tululu.org/l55/'

    title_page_urls = parse_tululu_category(category_url, start_page_id, end_page_id)
    books_summary = download_books(title_page_urls)
    
    with open('books.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_summary, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
