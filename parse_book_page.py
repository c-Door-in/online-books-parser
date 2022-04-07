import logging

from bs4 import BeautifulSoup


module_logger = logging.getLogger('log.parse_book_page')

def parse_title_and_author(soup):
    title_selector = '#content h1'
    title, author = soup.select_one(title_selector).text.split('::')
    return title.strip(), author.strip()


def parse_image_url(soup):
    image_selector = '.bookimage img'
    return soup.select_one(image_selector)['src']


def parse_txt_url(soup):
    link_selector = '.d_book a'
    for link_tag in soup.select(link_selector):
        if 'скачать txt' in link_tag.text:
            return link_tag['href']


def parse_genres(soup):
    genres_selector = 'span.d_book a'
    return [genre_tag.text for genre_tag in soup.select(genres_selector)]


def parse_comments(soup):
    comments_selector = '.texts span'
    return [comment_tag.text for comment_tag in soup.select(comments_selector)]


def parse_book_page(content):
    soup = BeautifulSoup(content, 'lxml')
    title, author = parse_title_and_author(soup)
    return {
        'title': title,
        'author': author,
        'image_url': parse_image_url(soup),
        'txt_url': parse_txt_url(soup),
        'genres': parse_genres(soup),
        'comments': parse_comments(soup),
    }