import json
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def get_index_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template('template.html')


def main():
    with open('./parsing_result/books.json', 'r', encoding='utf8') as file:
        books = json.load(file)
    
    for book in books:
        book['imagepath'] = quote(book['imagepath'])
        book['txtpath'] = quote(book['txtpath'])

    paged_books = list(chunked(books, 20))
    Path('pages').mkdir(parents=True, exist_ok=True)
    
    def on_reload():
        for page_num, page_books in enumerate(paged_books):
            books_pairs = list(chunked(page_books, 2))
            rendered_page = get_index_template().render(
                books_pairs = books_pairs
            )
            with open(f'pages/index{page_num}.html', 'w', encoding='utf8') as file:
                file.write(rendered_page)
        print('Site rebuilt')
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()