import argparse
import logging
import json
from pathlib import Path
from urllib.parse import urljoin

import requests
import urllib3
from bs4 import BeautifulSoup

from download_books import download_books


logger = logging.getLogger('log')


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
    parser.add_argument(
        '-f',
        '--dest_folder',
        default='parsing_result',
        help='Destination folder for downloaded parsing result',
    )
    parser.add_argument(
        '-i',
        '--skip_imgs',
        action='store_true',
        help='Bool argument to skip image downloading',
    )
    parser.add_argument(
        '-t',
        '--skip_txt',
        action='store_true',
        help='Bool argument to skip text downloading',
    )
    parser.add_argument(
        '-j',
        '--json_path',
        default='books',
        help='Set a path of the result json file',
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

    logger.info('Starting program')
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = create_arg_parser()
    args = parser.parse_args()

    if args.end_page and args.start_page > args.end_page:
        raise Exception('Start page number must be less than the end one')
    
    category_url = 'https://tululu.org/l55/'

    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    title_page_urls = parse_tululu_category(
        category_url,
        args.start_page,
        args.end_page,
    )
    books_summary = download_books(
        title_page_urls,
        args.dest_folder,
        args.skip_imgs,
        args.skip_txt,
    )
    
    with open(f'{args.dest_folder}/{args.json_path}.json', 'w', encoding='utf-8') as json_file:
        json.dump(books_summary, json_file, ensure_ascii=False)


if __name__ == '__main__':
    main()
