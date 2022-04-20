import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint
from urllib.parse import quote, urlencode, urljoin

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_index_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template('template.html')

# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()


def main():
    with open('./parsing_result/books.json', 'r', encoding='utf8') as file:
        books = json.load(file)
    
    for book in books:
        book['imagepath'] = quote(book['imagepath'])
        book['txtpath'] = quote(book['txtpath'])
    
    books_pairs = list(chunked(books, 2))
    
    def on_reload():
        rendered_page = get_index_template().render(
            books_pairs = books_pairs
        )
        with open('index.html', 'w', encoding='utf8') as file:
            file.write(rendered_page)
        print('Site rebuilt')
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()