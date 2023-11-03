import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('books'):
    os.makedirs('books')

base_url = 'https://tululu.org/b'
num_books = 10


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


for book_id in range(1, num_books + 1):
    url = base_url + str(book_id) + '/'

    if check_for_redirect(url):
        print(f"Книга {book_id} не доступна.")
        continue

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('title')
    if title_tag:
        full_title = title_tag.text.strip()
        book_title = full_title.split(' - ')[0]
        print(f"Название книги {book_id}: {book_title}")
    else:
        print(f"Не удалось найти название книги {book_id} на странице.")

    if response.ok:
        file_path = f'books/{book_title}.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(full_title + '\n\n')
            file.write(response.text)
        print(f"Книга {book_id} загружена успешно.")
    else:
        print(f"Не удалось скачать книгу {book_id}.")

print("Все книги скачаны.")