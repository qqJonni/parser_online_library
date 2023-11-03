import requests

url = 'https://tululu.org/txt.php?id=32168'

f = open("/Users/valeriy/Desktop/hlam/parser_online_library/peski_marsa.txt", 'wb')
response = requests.post(url)
f.write(response.content)
f.close()