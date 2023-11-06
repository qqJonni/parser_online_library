import requests
from bs4 import BeautifulSoup


num_books = 10

url = 'https://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('title')
image_url = soup.find('img', src='/shots/9.jpg')['src']
print(title_tag.text)
print(f'https://tululu.org{image_url}')
comments = soup.find('td', class_='ow_px_td').find_all('span', class_='black')
for comment in comments:
    print(comment.text)




