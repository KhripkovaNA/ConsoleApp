import os
import unittest
from unittest.mock import patch
from io import StringIO
from library import Library, Book
from service import add_book, update_status, search_books, delete_book

TEST_FILENAME = 'test_library.json'


class TestLibraryApp(unittest.TestCase):
    def setUp(self):
        """Создает тестовую библиотеку перед каждым тестом"""
        self.library = Library(TEST_FILENAME)
        Book._counter = 0

    def tearDown(self):
        """Удаляет тестовый файл после каждого теста."""
        if os.path.exists(TEST_FILENAME):
            os.remove(TEST_FILENAME)

    @patch("builtins.input", side_effect=["Книга 1", "Автор 1", "2023"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_book(self, mock_stdout, mock_input):
        """Тест на добавление книги"""
        add_book(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Книга 'Книга 1' добавлена с ID 1", output)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Книга 1")

    @patch("builtins.input", side_effect=["Книга 1", "Автор 1", "не известно", "отмена"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_add_book_cancel(self, mock_stdout, mock_input):
        """Тест на отмену добавления книги"""
        add_book(self.library)
        self.assertIn("Некорректный год издания!", mock_stdout.getvalue())
        self.assertIn("Добавление книги отменено", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_books_empty(self, mock_stdout):
        """Тест на отображение пустой библиотеки"""
        self.library.list_books()
        output = mock_stdout.getvalue()
        self.assertIn("Библиотека пуста", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_list_books(self, mock_stdout):
        """Тест на отображение всех книг в библиотеке"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.add_book("Книга 2", "Автор 2", 2021)
        self.library.list_books()
        output = mock_stdout.getvalue()
        self.assertIn("Список всех книг:", output)
        self.assertIn("Название: Книга 1", output)
        self.assertIn("Название: Книга 2", output)

    @patch("builtins.input", side_effect=["1", "выдана"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_status(self, mock_stdout, mock_input):
        """Тест на изменение статуса книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        update_status(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Статус книги с ID 1 успешно обновлен на 'выдана'", output)
        self.assertEqual(self.library.books[0].status, "выдана")

    @patch("builtins.input", side_effect=["не знаю", "отмена"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_status_cancel(self, mock_stdout, mock_input):
        """Тест на отмену изменения статуса книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        update_status(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Некорректный ID!", output)
        self.assertIn("Изменение статуса отменено", output)
        self.assertEqual(self.library.books[0].status, "в наличии")

    @patch("builtins.input", side_effect=["1", "не знаю", "отмена"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_status_cancel_2(self, mock_stdout, mock_input):
        """Тест на отмену изменения статуса книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        update_status(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Некорректный статус!", output)
        self.assertIn("Изменение статуса отменено", output)
        self.assertEqual(self.library.books[0].status, "в наличии")

    @patch("builtins.input", side_effect=["1", "выдана"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_update_status_existed(self, mock_stdout, mock_input):
        """Тест на изменение статуса книги на тот же"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.update_status(1, "выдана")
        update_status(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Статус книги с ID 1 уже 'выдана'", output)
        self.assertEqual(self.library.books[0].status, "выдана")

    @patch("builtins.input", side_effect=["1", "Книга 1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_books_name(self, mock_stdout, mock_input):
        """Тест на поиск книг по автору"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        search_books(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Найдена 1 книга", output)
        self.assertIn("Название: Книга 1", output)

    @patch("builtins.input", side_effect=["2", "Автор 1"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_books_author(self, mock_stdout, mock_input):
        """Тест на поиск книг по автору"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        self.library.add_book("Книга 2", "Автор 2", 2021)
        self.library.add_book("Книга 3", "Автор 1", 2022)
        search_books(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Найдено 2 книги", output)
        self.assertIn("Название: Книга 1", output)

    @patch("builtins.input", side_effect=["4", "отмена"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_books_cancel(self, mock_stdout, mock_input):
        """Тест на отмену поиска книг"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        search_books(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Некорректное поле поиска!", output)
        self.assertIn("Поиск книг отменен", output)

    @patch("builtins.input", side_effect=["1", "Книга 2"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_search_books_not_found(self, mock_stdout, mock_input):
        """Тест на поиск несуществующих книг"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        search_books(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Книги по заданному запросу не найдены", output)

    @patch("builtins.input", side_effect=["1", "да"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_book(self, mock_stdout, mock_input):
        """Тест на удаление книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        delete_book(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Книга с ID 1 успешно удалена", output)
        self.assertEqual(len(self.library.books), 0)

    @patch("builtins.input", side_effect=["не знаю", "отмена"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_book_cancel(self, mock_stdout, mock_input):
        """Тест на отмену удаления книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        delete_book(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Некорректный ID!", output)
        self.assertIn("Удаление отменено", output)
        self.assertEqual(len(self.library.books), 1)

    @patch("builtins.input", side_effect=["1", "нет"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_book_cancel_2(self, mock_stdout, mock_input):
        """Тест на отмену удаления книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        delete_book(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Удаление отменено", output)
        self.assertEqual(len(self.library.books), 1)

    @patch("builtins.input", side_effect=["2", "да"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_delete_book_not_found(self, mock_stdout, mock_input):
        """Тест на удаление несуществующей книги"""
        self.library.add_book("Книга 1", "Автор 1", 2020)
        delete_book(self.library)
        output = mock_stdout.getvalue()
        self.assertIn("Книга с ID 2 не найдена", output)
        self.assertEqual(len(self.library.books), 1)


if __name__ == "__main__":
    unittest.main()
