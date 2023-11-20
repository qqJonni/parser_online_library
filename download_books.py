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
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="""Программа скачивает книги. По умолчанию будут скачены книги с id 1 по 10""")
    parser.add_argument('start_id', nargs='?', help='Введите с какого id скачивать книги: ',
                        default=1, type=int)
    parser.add_argument('end_id', nargs='?', help='Введите до какого id скачивать книги: ',
                        default=10, type=int)

    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    return start_id, end_id


def get_filename_and_ext(img_url):
    """Get the link address and extension."""
    url_address = urlsplit(img_url).path
    encoding_url = unquote(url_address)
    filename = split(encoding_url)[-1]
    extension = splitext(filename)[-1]
    return filename, extension


def check_for_redirect(response):
    """Check for redirect in the HTTP response."""
    if response.history:
        final_url = response.url
        raise HTTPError(f"HTTPError: Redirect detected. Final URL: {final_url}")


def download_file(url, filename, folder='downloads/'):
    """Download a file from the given URL."""
    resource_path = Path(folder)
    resource_path.mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    normal_filename = sanitize_filename(filename)
    file_path = os.path.join(folder, normal_filename)
    with open(f'{file_path}', 'wb') as file:
        file.write(response.content)
    return file_path


def get_book_page(book_id):
    """Get the BeautifulSoup object for the book page."""
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_book_name(book_id):
    """Get the name of the book."""
    soup = get_book_page(book_id)
    title_tag = soup.find('td', class_='ow_px_td').find('div', id='content').find('h1')
    book_title = title_tag.text.split('::')[0].strip()
    book_name = f'{book_id}.{book_title}.txt'
    genres_tag = soup.find('span', class_='d_book').find_all('a')
    genres_text = [x.text for x in genres_tag]
    return book_name, book_title, genres_text


def fetch_book_comments(book_id, book_name):
    """Fetch and save book comments."""
    soup = get_book_page(book_id)
    book_comments = soup.find_all('div', class_='texts')
    comments_path = Path('comments')
    comments_path.mkdir(parents=True, exist_ok=True)
    normal_book_name = sanitize_filename(book_name)
    file_path = os.path.join(comments_path, normal_book_name)
    with open(file_path, "w", encoding='utf-8') as file:
        for comment in book_comments:
            file.write(comment.span.string + '\n')
    return 'success'


def get_img_url_name(book_id):
    """Get the URL and name of the book cover image."""
    url = 'https://tululu.org/'
    soup = get_book_page(book_id)
    img = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(url, img)
    img_name, _ = get_filename_and_ext(img_url)
    return img_url, img_name


def fetch_books(start_id, end_id):
    """Fetch and download books within the specified range of IDs."""
    book_id = start_id
    while book_id <= end_id:
        try:
            url = 'https://tululu.org/txt.php'
            params = {'id': book_id}
            response = requests.get(url, params=params, allow_redirects=False)
            check_for_redirect(response)
            response.raise_for_status()
            book_url = response.url
            book_name, book_title, genres_text = get_book_name(book_id)
            print(f'{book_title}\n{genres_text}\n')
            fetch_book_comments(book_id, book_name)
            download_file(book_url, book_name)
            img_url, img_name = get_img_url_name(book_id)
            download_file(img_url, img_name)

            book_id += 1
        except HTTPError as e:
            print(f"HTTPError: Failed to fetch book with ID {book_id}. Error: {e}")
            book_id += 1
        except (AttributeError, ConnectionError) as e:
            print(f"Error: Failed to fetch book with ID {book_id}. Error: {e}")
            book_id += 1


def main():
    start_id, end_id = get_command_line_argument()
    fetch_books(start_id, end_id)


if __name__ == '__main__':
    main()
