import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urljoin

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


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
    category_url = 'https://tululu.org/l55/'
    for book in books:
        book['image_url'] = urljoin(category_url, book['image_url'])

    
    def on_reload():
        rendered_page = get_index_template().render(
            books=books,
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