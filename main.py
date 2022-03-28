import argparse

import requests
import urllib3
from bs4 import BeautifulSoup

from download_image import download_image
from download_txt import download_txt, compose_text_filename, get_title_and_author


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog='TULULU PARSER',
        description='Parser for online-library tululu.org',
    )
    parser.add_argument(
        'start_id',
        help='Set start book ID for parsing range',
        type=int,
    )
    parser.add_argument(
        'end_id',
        help='Set end book ID for parsing range',
        type=int,
    )
    return parser


def check_for_redirect(source_url, response):
    if not response.history:
        return
    if source_url not in response.url:
        raise requests.HTTPError


def fetch_book(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(url, response)
    return response.text


def parse_title_and_author(soup):
    title_tag = soup.find('div', id='content').find('h1')
    title, author = title_tag.text.split('::')
    return title.strip(), author.strip()


def parse_image_url(soup):
    image_tag = soup.find('div', class_='bookimage').find('img')
    return image_tag['src']


def parse_txt_url(soup):
    book_menu_links = soup.find('table', class_='d_book').find_all('a')
    for link in book_menu_links:
        if 'скачать txt' in link.text:
            return link['href']


def parse_genres(soup):
    for tag in soup.find_all('span', class_='d_book'):
        if 'Жанр книги' in tag.text:
            return [genre_tag.text for genre_tag in tag.find_all('a')]


def parse_comments(soup):
    comments_tags = soup.find_all('div', class_='texts')
    return [comment.find('span').text for comment in comments_tags]


def parse_book_page(content):
    soup = BeautifulSoup(content, 'lxml')
    title, author = parse_title_and_author(soup)
    return {
        'title': title,
        'author': author,
        'image_url': parse_image_url(soup),
        'txt_url': parse_txt_url(soup),
        'genres': parse_genres(soup),
        'comments': parse_comments(soup),
    }


def download_book(book_id):
    title_url = f'https://tululu.org/b{book_id}/'
    book_page = fetch_book(title_url)
    # download_txt(book_text, text_filename)
    # download_image(title_url, book_title)
    # download_comments(title_page_soup)
    print(parse_book_page(book_page))



def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = create_arg_parser()
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    if start_id > end_id:
        start_id, end_id = end_id, start_id
    for book_id in range(start_id, end_id+1):
        try:
            download_book(book_id)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()