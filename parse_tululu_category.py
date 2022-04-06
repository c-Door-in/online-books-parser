import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def is_final_page(soup, page_id):
    return str(page_id) not in [
        npage.text for npage in soup.find('div', id='content') \
                                    .find_all('a', class_='npage')
    ]


def parse_books_url(soup):
    book_cards = soup.find_all('table', class_='d_book')
    return [card.find('a')['href'] for card in book_cards]


def parse_tululu_category(category_url, pages_count, start_page_id=1):
    book_urls = list()
    page_id = start_page_id
    while True:
        print(page_id)
        list_page_url = f'{category_url}{page_id}/'
        response = requests.get(list_page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        for book_url in parse_books_url(soup):
            book_urls.extend([urljoin(category_url, book_url)])
        page_id += 1
        if is_final_page(soup, page_id) or page_id > pages_count:
            break
        
    return book_urls


def main():
    category_url = 'https://tululu.org/l55/'
    pages_count = 4
    for id, book_url in enumerate(parse_tululu_category(category_url, pages_count)):
        print(id, book_url)


if __name__ == '__main__':
    main()
