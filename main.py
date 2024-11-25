import os
from library import Library


def main():
    library = Library('data.json')
    while True:
        print("Меню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Выберите действие: ")

        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            confirmation = input(f"Вы уверены, что хотите удалить книгу с ID {book_id}? (да/нет): ").lower()
            if confirmation == "да":
                library.delete_book(book_id)
            else:
                print("Удаление отменено")

        elif choice == "3":
            field = input("Поле для поиска (1 - по названию, 2 - по автору, 3 - по году выпуска): ")
            query = input("Введите запрос: ")
            library.search_books(field, query)

        elif choice == "4":
            library.list_books()

        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_status = input("Введите новый статус: ")
            library.update_status(book_id, new_status)

        elif choice == "6":
            print("Завершение работы")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
