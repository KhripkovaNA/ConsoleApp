def conjugate_books(number: int) -> str:
    last_digit = number % 10
    last_two_digits = number % 100

    if 10 <= last_two_digits <= 20:
        return f"Найдено {number} книг:"
    elif last_digit == 1:
        return f"Найдена {number} книга:"
    elif 2 <= last_digit <= 4:
        return f"Найдено {number} книги:"
    else:
        return f"Найдено {number} книг:"


def present_book(book: "Book") -> str:
    return (
        f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
    )
