import unittest
from unittest.mock import patch
import io
import os
from library import Book, Library

TEST_FILENAME = 'test_library.json'


class TestLibraryApp(unittest.TestCase):
    def setUp(self):
        """Создает тестовую библиотеку перед каждым тестом"""
        self.library = Library(TEST_FILENAME)
        Book._counter = 0

    def tearDown(self):
        """Удаляет тестовый файл после каждого теста"""
        if os.path.exists(TEST_FILENAME):
            os.remove(TEST_FILENAME)

    def test_add_book(self):
        """Тест на добавление книги"""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.add_book("Книга 1", "Автор 1", "2023")
            output = fake_out.getvalue()
        self.assertIn("Книга 'Книга 1' добавлена с ID 1", output)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Книга 1")

    def test_delete_book(self):
        """Тест на удаление книги"""
        self.library.add_book("Книга для удаления", "Автор", "2022")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.delete_book("1")
            output = fake_out.getvalue()
        self.assertIn("Книга с ID 1 успешно удалена", output)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        """Тест на поиск книги"""
        self.library.add_book("Книга для поиска", "Автор", "2021")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.search_books("1", "Книга для поиска")
            output = fake_out.getvalue()
        self.assertIn("Найдена 1 книга", output)
        self.assertIn("Название: Книга для поиска", output)

    def test_list_books_empty(self):
        """Тест на отображение пустой библиотеки"""
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.list_books()
            output = fake_out.getvalue()
        self.assertIn("Библиотека пуста", output)

    def test_list_books(self):
        """Тест на отображение всех книг в библиотеке"""
        self.library.add_book("Книга 1", "Автор 1", "2020")
        self.library.add_book("Книга 2", "Автор 2", "2021")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.list_books()
            output = fake_out.getvalue()
        self.assertIn("Список всех книг:", output)
        self.assertIn("Название: Книга 1", output)
        self.assertIn("Название: Книга 2", output)

    def test_update_status(self):
        """Тест на изменение статуса книги"""
        self.library.add_book("Книга 1", "Автор 1", "2020")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.update_status("1", "выдана")
            output = fake_out.getvalue()
        self.assertIn("Статус книги с ID 1 успешно обновлен на 'выдана'", output)
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_update_status_invalid(self):
        """Тест на изменение статуса книги на некорректный"""
        self.library.add_book("Книга 1", "Автор 1", "2020")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            self.library.update_status("1", "неизвестен")
            output = fake_out.getvalue()
        self.assertIn("Некорректный статус. Используйте: 'в наличии' или 'выдана'", output)
        self.assertEqual(self.library.books[0].status, "в наличии")


if __name__ == "__main__":
    unittest.main()
