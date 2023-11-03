import requests
import os
if not os.path.exists('books'):
    os.makedirs('books')


base_url = 'https://tululu.org/txt.php?id='
num_books = 10

for book_id in range(1, num_books + 1):

    url = base_url + str(book_id)

    response = requests.get(url)
    if response.status_code == 200:

        file_path = f'books/book_{book_id}.txt'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Book {book_id} downloaded successfully.")
    else:
        print(f"Failed to download book {book_id}.")

print("All books downloaded.")
