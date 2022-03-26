import requests
import urllib3

from download_image import download_image
from download_txt import download_txt, compose_text_filename


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