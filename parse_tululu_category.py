import argparse
import json
from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup

from download_books import download_books


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
        default=1,
        help='Set end book ID for parsing range',
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


def parse_tululu_category(category_url, pages_count=None, start_page_id=1):
    book_urls = list()
    page_id = start_page_id
    while True:
        print(page_id)
        list_page_url = f'{category_url}{page_id}/'
        response = requests.get(list_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for book_url in parse_book_urls(soup):
            book_urls.extend([urljoin(category_url, book_url)])
        page_id += 1
        if is_final_page(soup, page_id):
            break
        if pages_count:
            if page_id > pages_count:
                break
        
    return book_urls


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
    pages_count = 1
    for id, book_url in enumerate(parse_tululu_category(category_url, pages_count)):
        print(id, book_url)

    title_page_urls = parse_tululu_category(category_url, 1)
    books_summary = download_books(title_page_urls)
    
    with open('books.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_summary, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
