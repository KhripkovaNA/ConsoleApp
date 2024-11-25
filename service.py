from library import Library


def add_book(library: Library) -> None:
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    while True:
        user_input = input("Введите год издания: ")
        if user_input == "отмена":
            break
        else:
            try:
                year = int(user_input)
                library.add_book(title, author, year)
                break
            except ValueError:
                print("Некорректный год издания!")
                print("Введите корректный год или введите 'отмена' для возврата в основное меню")


def update_status(library: Library) -> None:
    book_id = None
    while True:
        if book_id is None:
            user_input = input("Введите ID книги для изменения статуса: ")
            if user_input == "отмена":
                break
            else:
                try:
                    book_id = int(user_input)
                except ValueError:
                    print("Некорректный ID!")
                    print("Введите корректный ID или введите 'отмена' для возврата в основное меню")
                    continue
        new_status = input("Введите новый статус: ")
        if new_status == "отмена":
            break
        elif new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус!")
            print("Используйте: 'в наличии' или 'выдана' или введите 'отмена' для возврата в основное меню")
        else:
            library.update_status(book_id, new_status)
            break


def search_books(library: Library) -> None:
    while True:
        user_input = input("Поле для поиска (1 - по названию, 2 - по автору, 3 - по году выпуска): ")
        if user_input == "отмена":
            break
        else:
            field_map = {"1": "title", "2": "author", "3": "year"}
            if user_input not in field_map:
                print("Некорректное поле поиска!")
                print("Используйте: 1 - по названию, 2 - по автору, 3 - по году выпуска "
                      "или введите 'отмена' для возврата в основное меню")
                continue
            field = field_map[user_input]
        query = input("Введите запрос: ")
        library.search_books(field, query)
        break


def delete_book(library: Library) -> None:
    while True:
        user_input = input("Введите ID книги для удаления: ")
        if user_input == "отмена":
            break
        else:
            try:
                book_id = int(user_input)
                confirmation = input(f"Вы уверены, что хотите удалить книгу с ID {book_id}? (да/нет): ").lower()
                if confirmation == "да":
                    library.delete_book(book_id)
                else:
                    print("Удаление отменено")
                break
            except ValueError:
                print("Некорректный ID!")
                print("Введите корректный ID или введите 'отмена' для возврата в основное меню")
