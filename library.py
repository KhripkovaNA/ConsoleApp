import json
from typing import List, Optional, Dict
from utils import conjugate_books, present_book


class Book:
    _counter = 0

    def __init__(self, title: str, author: str, year: int, status: str = "в наличии"):
        Book._counter += 1
        self.id = Book._counter
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        """Преобразует объект книги в словарь для сохранения в JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict) -> "Book":
        """Создает объект книги из словаря"""
        return Book(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = self.load_books()

    def load_books(self) -> List[Book]:
        """Загружает книги из JSON файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                books = json.load(file)
                return [Book.from_dict(book) for book in books]
        except FileNotFoundError:
            return []

    def save_books(self) -> None:
        """Сохраняет данные в JSON файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: str) -> None:
        """Добавляет новую книгу в библиотеку"""
        try:
            year = int(year)
        except ValueError:
            print('Некорректный год издания!')
            return
        new_book = Book(title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {new_book.id}")

    def delete_book(self, book_id: str) -> None:
        """Удаляет книгу по ID"""
        try:
            book_id = int(book_id)
        except ValueError:
            print('Некорректный ID!')
            return
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} успешно удалена")
                return
        print(f"Книга с ID {book_id} не найдена")

    def search_books(self, field: str, query: str) -> None:
        """Ищет книги по заданному полю"""
        field_map = {"1": "title", "2": "author", "3": "year"}
        if field not in field_map:
            print("Некорректное поле поиска. Используйте: 1 - по названию, 2 - по автору, 3 - по году выпуска")
            return
        attribute = field_map[field]
        results = [
            present_book(book)
            for book in self.books
            if query.lower() in str(getattr(book, attribute, "")).lower()
        ]
        if results:
            print(conjugate_books(len(results)))
            print(*results, sep='\n')
        else:
            print("Книги по заданному запросу не найдены")

    def list_books(self) -> None:
        """Отображает все книги в библиотеке"""
        if not self.books:
            print("Библиотека пуста")
        else:
            print("Список всех книг:")
            for book in self.books:
                print(present_book(book))

    def update_status(self, book_id: str, new_status: str) -> None:
        """Обновляет статус книги по ID"""
        try:
            book_id = int(book_id)
        except ValueError:
            print('Некорректный ID!')
            return
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Используйте: 'в наличии' или 'выдана'")
            return
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                print(f"Статус книги с ID {book_id} успешно обновлен на '{new_status}'")
                return
        print(f"Книга с ID {book_id} не найдена")
