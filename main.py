import os

from pathlib import Path

import requests
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(source_url, response):
    if not response.history:
        return
    if source_url not in response.url:
        raise requests.HTTPError


def fetch_book(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(url, response)
    return response


def get_title_and_author(book_title_url):
    response = fetch_book(book_title_url)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')
    title, author = title_tag.text.split('::')
    return title.strip(), author.strip()


def compose_filename(book_id, book_title_url):
    title, author = get_title_and_author(book_title_url)
    return f'{book_id}. {title}.txt'


def download_txt(url, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    response = fetch_book(url)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(response.text)
    return filepath


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    count = 10
    for book_id in range(1, count+1):
        book_title_url = f'https://tululu.org/b{book_id}/'
        text_url = f'https://tululu.org/txt.php?id={book_id}'
        try:
            filename = compose_filename(book_id, book_title_url)
            download_txt(text_url, filename)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()