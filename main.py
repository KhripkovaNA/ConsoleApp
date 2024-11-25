from library import Library
from service import add_book, update_status, search_books, delete_book

FILENAME = 'library.json'


def main():
    library = Library(FILENAME)

    while True:
        print("Меню:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Изменить статус книги")
        print("4. Найти книгу")
        print("5. Удалить книгу")
        print("6. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":  # Добавить книгу
            add_book(library)

        elif choice == "2":  # Показать все книги
            library.list_books()

        elif choice == "3":  # Изменить статус книги
            update_status(library)

        elif choice == "4":  # Найти книгу
            search_books(library)

        elif choice == "5":  # Удалить книгу
            delete_book(library)

        elif choice == "6":  # Выход
            print("Завершение работы")
            break

        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
