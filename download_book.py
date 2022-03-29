import requests

from download_image import download_image
from download_txt import download_txt
from parse_book_page import parse_book_page


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


def download_book(book_id):
    title_url = f'https://tululu.org/b{book_id}/'
    book_page = fetch_book(title_url)
    parsed_page = parse_book_page(book_page)

    title = parsed_page['title']
    txt_url = parsed_page['txt_url']
    image_url = parsed_page['image_url']
    if not txt_url:
        return
    download_txt(title_url, txt_url, book_id, title)
    download_image(title_url, image_url)