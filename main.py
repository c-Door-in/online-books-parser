import argparse

import requests
import urllib3

from download_book import download_book


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


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = create_arg_parser()
    args = parser.parse_args()
    
    start_id, end_id = args.start_id, args.end_id
    if start_id > end_id:
        start_id, end_id = end_id, start_id
    print(f'parsing from {start_id} to {end_id}')
    for book_id in range(start_id, end_id+1):
        try:
            download_book(book_id)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()