import os

from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

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
    return response.text


def get_title_and_author(soup):
    title_tag = soup.find('div', id='content').find('h1')
    title, author = title_tag.text.split('::')
    return title.strip(), author.strip()


def compose_text_filename(book_title, book_id):
    soup = BeautifulSoup(book_title, 'lxml')
    title, author = get_title_and_author(soup)
    filename = sanitize_filename(f'{book_id}. {title}.txt')
    return filename


def download_txt(book_text, filename, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as file:
        file.write(book_text)
    return filepath


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


def download_book(book_id):
    text_url = f'https://tululu.org/txt.php?id={book_id}'
    book_text = fetch_book(text_url)

    title_url = f'https://tululu.org/b{book_id}/'
    book_title = fetch_book(title_url)

    text_filename = compose_text_filename(book_title, book_id)
    download_txt(book_text, text_filename)
    download_image(title_url, book_title)



def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    count = 10
    for book_id in range(1, count+1):
        try:
            download_book(book_id)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()