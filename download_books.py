import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os


def check_for_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content_type = soup.find('meta', {'http-equiv': 'Content-Type'})

        if content_type and content_type.get('content', '').lower() == 'text/html;charset=windows-1251':
            raise requests.exceptions.HTTPError(f"Invalid content type for URL: {url}")
        if response.history:
            print(f"Redirected to: {response.url}")
            return True

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return True
    return False


def parse_book_title(book_id):
    url = f'{base_url}{book_id}/'
    if check_for_redirect(url):
        print(f"Книга {book_id} не доступна.")
        return None

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('title')
    if title_tag:
        full_title = title_tag.text.strip()
        book_title = full_title.split(' - ')[0]
        return book_title
    else:
        print(f"Не удалось найти название книги {book_id} на странице.")
        return None


def download_book(book_id, book_title):
    url = f'{base_url}{book_id}/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Генерировать исключение, если возникла ошибка в запросе
    except requests.exceptions.RequestException as e:
        print(f"Не удалось скачать книгу {book_id}. Ошибка: {e}")
        return

    file_path = f'books/{book_title}.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(book_title + '\n\n')
        file.write(response.text)
    print(f"Книга {book_id} загружена успешно.")


def download_image(book_id):
    url = f'https://tululu.org/shots/{book_id}.jpg'
    image_response = requests.get(url)
    if image_response.ok:
        image_path = f'images/{book_id}.jpg'
        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Обложка книги {book_id} загружена успешно.")
    else:
        print(f"Не удалось найти обложку книги {book_id} на странице.")


def download_books(start_id, end_id):
    for book_id in tqdm(range(start_id, end_id + 1)):
        book_title = parse_book_title(book_id)
        if book_title is not None:
            download_book(book_id, book_title)
            download_image(book_id)

    print("Все книги и обложки скачаны.")


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    parser = argparse.ArgumentParser(description="Download books and images from tululu.org")
    parser.add_argument("--start_id", type=int, default=1, help="Start book ID")
    parser.add_argument("--end_id", type=int, default=10, help="End book ID")
    args = parser.parse_args()
    base_url = 'https://tululu.org/b'
    download_books(args.start_id, args.end_id)
