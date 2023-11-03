import requests

import os
if not os.path.exists('books'):
    os.makedirs('books')

base_url = 'https://tululu.org/txt.php?id='
num_books = 8


def check_for_redirect(url):
    try:
        response = requests.head(url)
        if response.headers.get('Content-Type') == 'text/html;charset=windows-1251':
            raise requests.exceptions.HTTPError(f"Неверный тип контента для URL: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return True
    return False


for book_id in range(1, num_books + 1):
    url = base_url + str(book_id)

    if check_for_redirect(url):
        print(f"Книга {book_id} не доступна.")
        continue

    response = requests.get(url)
    if response.status_code == 200:
        file_path = f'books/book_{book_id}.txt'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Книга {book_id} загружена успешно.")
    else:
        print(f"Не удалось скачать книгу {book_id}.")

print("Все книги скачаны.")
