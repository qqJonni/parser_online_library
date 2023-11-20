import os
import requests
import argparse
from pathlib import Path
from os.path import split, splitext
from pathvalidate import sanitize_filename
from requests import HTTPError, ConnectionError
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, unquote


def get_command_line_argument():
    """parse args"""
    parser = argparse.ArgumentParser(
        description="""Программа скачивает книги. по дефолту будут скачены книги с id 1 по 10 """)
    parser.add_argument('start_id', nargs='?', help='Введите с какого id скачивать книги: ',
                        default=1, type=int)
    parser.add_argument('end_id', nargs='?', help='Введите до какого id скачивать книги: ',
                        default=10, type=int)

    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    return start_id, end_id


def get_filename_and_ext(img_url):
    """Getting the link address and extension"""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def check_for_redirect(response):
    if response.status_code > 204:
        raise HTTPError


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)


def download_image(url, filename, folder='images/'):
    """Функция для скачивания изображений.
    Args:
        url (str): Cсылка на картинку, которую хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    book_path = Path(folder)
    book_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_name(book_id):
    soup = parse_book_page(book_id)
    title_tag = soup.find('td', class_='ow_px_td').find('div', id='content').find('h1')
    book_title = title_tag.text.split('::')[0].strip()
    book_name = f'{book_id}.{book_title}.txt'
    genres_tag = soup.find('span', class_='d_book').find_all('a')
    genres_text = [x.text for x in genres_tag]
    print(f'{book_title}\n{genres_text}\n')
    return book_name


def fetch_book_comments(book_id, book_name):
    soup = parse_book_page(book_id)
    book_comments = soup.find_all('div', class_='texts')
    book_path = Path('comments')
    book_path.mkdir(parents=True, exist_ok=True)
    normal_book_name = sanitize_filename(book_name)
    file_path = os.path.join(book_path, normal_book_name)
    with open(f"{file_path}", "w", encoding='utf-8') as file:
        for comment in book_comments:
            file.write(comment.span.string + '\n')
    return 'success'


def get_img_url_name(book_id):
    url = 'https://tululu.org/'
    soup = parse_book_page(book_id)
    img = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(url, img)
    img_name, _ = get_filename_and_ext(img_url)
    return img_url, img_name


def fetch_books(start_id, end_id):
    book_id = start_id
    while book_id <= end_id:
        try:
            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            response = requests.get(url, params=params, allow_redirects=False)
            check_for_redirect(response)
            response.raise_for_status()
            book_url = response.url
            book_name = get_book_name(book_id)
            fetch_book_comments(book_id, book_name)
            download_txt(book_url, book_name)
            img_url, img_name = get_img_url_name(book_id)
            download_image(img_url, img_name)

            book_id += 1
        except (HTTPError, AttributeError, ConnectionError):
            book_id += 1


def main():
    start_id, end_id = get_command_line_argument()
    fetch_books(start_id, end_id)


if __name__ == '__main__':
    main()
