# Название: Парсим онлайн-библиотеку

Приложение может загружать книги и обложки книг, а так же выводить название и жанр книги

![скрин](https://dvmn.org/media/lessons/books_1_F7MUA7w.jpg)


### Окружение: Как установить

* Скачать [этот script](https://github.com/qqJonni/space_photos.git)

**Python 3.11 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:

**Создаём и активируем виртуальное окружение:**

Для MacOS: Обычно окружение создается командой python3 -m venv имя_окружения; source имя_окружения/bin/activate

Для Windows: C:\> имя_окружения\Scripts\activate.bat


### Зависимости
```properties
pip install -r requirements.txt
```

### Запуск

Эта команда скачивает книги и картинки.
```properties
python download_books.py --start_id 5 --end_id 10
```
Эта команда отображает название книг и жанр
```properties
parse_book_page.py --start_id 5 --end_id 10
```
### Примечания

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
