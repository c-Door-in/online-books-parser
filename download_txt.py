import os
from pathlib import Path

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


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