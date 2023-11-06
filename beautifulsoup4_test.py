import requests
from bs4 import BeautifulSoup


url = 'https://tululu.org/b9/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
image_url = soup.find('img', src='/shots/9.jpg')['src']
print(f'https://tululu.org{image_url}')