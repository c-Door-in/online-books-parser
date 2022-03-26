from download_txt import get_title_and_author


def download_comments(soup):
    title, author = get_title_and_author(soup)
    comments_tags = soup.find_all('div', class_='texts')
    print(title)
    for tag in comments_tags:
        print(tag.find('span').text)
    print('\n\n')
    return