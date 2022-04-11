import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urljoin

from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

with open('./parsing_result/books.json', 'r', encoding='utf8') as file:
    books = json.load(file)

category_url = 'https://tululu.org/l55/'
for book in books:
    book['image_url'] = urljoin(category_url, book['image_url'])


rendered_page = template.render(
    books=books,
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()