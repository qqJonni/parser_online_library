# Название: Парсим онлайн-библиотеку

Приложение может загружать книги и обложки книг, а так же выводить название и жанр книги

![скрин](https://dvmn.org/media/lessons/books_1_F7MUA7w.jpg)


### Окружение: Как установить

* Скачать [этот script](https://github.com/qqJonni/space_photos.git)

**Python 3.11 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:

**Создаём и активируем виртуальное окружение:**
```properties
Для MacOS: Обычно окружение создается командой python3 -m venv имя_окружения; source имя_окружения/bin/activate
```
```properties
Для Windows: C:\> имя_окружения\Scripts\activate.bat
```

### Зависимости
```properties
pip install -r requirements.txt
```

### Запуск

При запуске программы используйте аргументы `--start_page` и `--end_page`.
Например:
```properties
python download_books.py 20 30
```
Без указания аргументов дефолтные значения `--start_page` и `--end_page` равны 1 и 10.
### Примечания

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
