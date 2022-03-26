import requests
import urllib3
from bs4 import BeautifulSoup

from download_image import download_image
from download_txt import download_txt, compose_text_filename, get_title_and_author
from download_comments import download_comments


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


def parse_genres(soup):
    genre_tag = soup.find('span', class_='d_book').find('a')
    return genre_tag.text


def download_book(book_id):
    text_url = f'https://tululu.org/txt.php?id={book_id}'
    book_text = fetch_book(text_url)

    title_url = f'https://tululu.org/b{book_id}/'
    book_title = fetch_book(title_url)
    title_page_soup = BeautifulSoup(book_title, 'lxml')

    text_filename = compose_text_filename(book_title, book_id)
    title, author = get_title_and_author(title_page_soup)
    # download_txt(book_text, text_filename)
    # download_image(title_url, book_title)
    # download_comments(title_page_soup)
    print('Заголовок:', title)
    print(parse_genres(title_page_soup))



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