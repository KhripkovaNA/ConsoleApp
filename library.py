import json
from typing import List, Dict
from utils import conjugate_books, present_book


class Book:
    _counter = 0

    def __init__(self, title: str, author: str, year: int, book_id: int = None, status: str = "в наличии"):
        if book_id is None:
            Book._counter += 1
            self.id = Book._counter
        else:
            self.id = book_id
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
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )


class Library:
    def __init__(self, filename: str):
        self.filename = filename
        self.books: List[Book] = self.load_books()
        Book._counter = self.books[-1].id

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

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет новую книгу в библиотеку"""
        new_book = Book(title=title, author=author, year=year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {new_book.id}")

    def list_books(self) -> None:
        """Отображает все книги в библиотеке"""
        if not self.books:
            print("Библиотека пуста")
        else:
            print("Список всех книг:")
            for book in self.books:
                print(present_book(book))

    def update_status(self, book_id: int, new_status: str) -> None:
        """Обновляет статус книги по ID"""
        for book in self.books:
            if book.id == book_id:
                if book.status != new_status:
                    book.status = new_status
                    self.save_books()
                    print(f"Статус книги с ID {book_id} успешно обновлен на '{new_status}'")
                else:
                    print(f"Статус книги с ID {book_id} уже '{new_status}'")
                return
        print(f"Книга с ID {book_id} не найдена")

    def search_books(self, field: str, query: str) -> None:
        """Ищет книги по заданному полю"""
        results = [
            present_book(book)
            for book in self.books
            if query.lower() in str(getattr(book, field, "")).lower()
        ]
        if results:
            print(conjugate_books(len(results)))
            print(*results, sep='\n')
        else:
            print("Книги по заданному запросу не найдены")

    def delete_book(self, book_id: int) -> None:
        """Удаляет книгу по ID"""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} успешно удалена")
                return
        print(f"Книга с ID {book_id} не найдена")
