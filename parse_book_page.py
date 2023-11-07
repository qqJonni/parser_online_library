import argparse
import requests
from bs4 import BeautifulSoup


def check_for_redirect(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.history:
            for resp in response.history:
                print(f"Redirected to: {resp.url}")
            return True
        else:
            return False
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return True


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
            print(genre, '\n')
        else:
            print('Жанр не определен')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download books from tululu.org")
    parser.add_argument("--start_id", type=int, default=1, help="Start page ID")
    parser.add_argument("--end_id", type=int, default=10, help="End page ID")
    args = parser.parse_args()
    base_url = f'https://tululu.org/b{args.start_id}'

    for page_id in range(args.start_id, args.end_id + 1):
        current_url = f'https://tululu.org/b{page_id}'
        parse_book_page(current_url)
