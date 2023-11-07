import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

os.makedirs('books', exist_ok=True)
os.makedirs('images', exist_ok=True)


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


def download_books(start_id, end_id):
    for book_id in tqdm(range(start_id, end_id + 1)):
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

        image_url = soup.find('img', src='/shots/{}.jpg'.format(book_id))
        if image_url:
            image_url = 'https://tululu.org' + image_url['src']
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_path = f'images/{book_id}.jpg'
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Обложка книги {book_id} загружена успешно.")
        else:
            print(f"Не удалось найти обложку книги {book_id} на странице.")

    print("Все книги и обложки скачаны.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download books and images from tululu.org")
    parser.add_argument("--start_id", type=int, default=1, help="Start book ID")
    parser.add_argument("--end_id", type=int, default=10, help="End book ID")
    args = parser.parse_args()
    base_url = 'https://tululu.org/b'
    download_books(args.start_id, args.end_id)
