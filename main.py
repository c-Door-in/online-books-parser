import requests
# import urllib3

from pathlib import Path


def main():
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    book_dir = 'books'
    Path(book_dir).mkdir(parents=True, exist_ok=True)
    
    url = 'https://tululu.org/txt.php'
    for book_id in range(1, 11):
        payload = {'id': book_id}
        response = requests.get(url, params=payload)
        response.raise_for_status()

        filename = f'id{book_id}.txt'
        with open(f'{book_dir}/{filename}', 'w') as file:
            file.write(response.text)


if __name__ == '__main__':
    main()