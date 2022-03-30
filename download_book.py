import requests

from download_image import download_image
from download_txt import download_txt
from parse_book_page import parse_book_page


def download_book(book_id):
    title_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(title_url)
    response.raise_for_status()
    if response.history:
        raise requests.HTTPError
    parsed_page = parse_book_page(response.text)
    title = parsed_page['title']
    txt_url = parsed_page['txt_url']
    image_url = parsed_page['image_url']
    if not txt_url:
        return
    download_txt(title_url, txt_url, book_id, title)
    download_image(title_url, image_url)