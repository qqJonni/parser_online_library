import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('books'):
    os.makedirs('books')

if not os.path.exists('images'):
    os.makedirs('images')

base_url = 'https://tululu.org/b1'


def check_for_redirect(url):
    try:
        response = requests.head(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content_type = soup.find('meta', {'http-equiv': 'Content-Type'})
        if content_type and content_type['content'] == 'text/html;charset=windows-1251':
            raise requests.exceptions.HTTPError(f"Неверный тип контента для URL: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return True
    return False


def parse_book_page(url):
    if check_for_redirect(url):
        print(f"Книга не доступна.")
    else:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('title')
        genre_info_element = soup.find('span', class_='d_book')

        if title_tag:
            full_title = title_tag.text.strip()
            book_title = full_title.split(' - ')[0]
            print(f"Название книги: {book_title}")
        else:
            print(f"Не удалось найти название книги на странице.")

        if genre_info_element:
            genre_info = genre_info_element.find('a')['title']
            genre = genre_info.split(' - ')[0]
            print(genre)
        else:
            print('Жанр не определен')

parse_book_page(base_url)
