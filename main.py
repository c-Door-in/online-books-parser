from urllib.error import HTTPError
import requests
# import urllib3

from pathlib import Path


def check_for_redirect(source_url, response):
    if not response.history:
        return
    if source_url not in response.url:
        raise requests.HTTPError


def fetch_books(source_url, book_id):
    payload = {'id': book_id}
    response = requests.get(source_url, params=payload)
    response.raise_for_status()
    check_for_redirect(source_url, response)
    return response


def download_books(source_url, book_dir, count):
    Path(book_dir).mkdir(parents=True, exist_ok=True)
    for book_id in range(1, count+1):
        try:
            response = fetch_books(source_url, book_id)
        except requests.HTTPError:
            continue

        filename = f'id{book_id}.txt'
        with open(f'{book_dir}/{filename}', 'w') as file:
            file.write(response.text)


def main():
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    books_source_url = 'https://tululu.org/txt.php'
    download_books(books_source_url, 'books', 10)
    
    
    


if __name__ == '__main__':
    main()