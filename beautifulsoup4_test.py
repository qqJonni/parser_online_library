import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b1/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('title')
print(title_tag.text)