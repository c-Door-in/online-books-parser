from bs4 import BeautifulSoup


def parse_title_and_author(soup):
    title_tag = soup.find('div', id='content').find('h1')
    title, author = title_tag.text.split('::')
    return title.strip(), author.strip()


def parse_image_url(soup):
    image_tag = soup.find('div', class_='bookimage').find('img')
    return image_tag['src']


def parse_txt_url(soup):
    book_menu_links = soup.find('table', class_='d_book').find_all('a')
    for link in book_menu_links:
        if 'скачать txt' in link.text:
            return link['href']


def parse_genres(soup):
    for tag in soup.find_all('span', class_='d_book'):
        if 'Жанр книги' in tag.text:
            return [genre_tag.text for genre_tag in tag.find_all('a')]


def parse_comments(soup):
    comments_tags = soup.find_all('div', class_='texts')
    return [comment.find('span').text for comment in comments_tags]


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