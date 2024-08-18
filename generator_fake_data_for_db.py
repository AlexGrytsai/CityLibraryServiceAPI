import json
import random

from faker import Faker

fake = Faker()


def generate_fake_user_data() -> list:
    users_data = []
    for i in range(100):
        pk = i + 30
        email = fake.unique.email(domain="example.com")
        first_name = fake.first_name()
        last_name = fake.last_name()
        user = {
            "model": "users.user",
            "pk": pk,
            "fields": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
            },
        }

        users_data.append(user)
    return users_data


def generate_fake_books_data_for_db() -> list:
    books_data = []
    for i in range(1100):
        pk = i + 30
        title = fake.unique.sentence(nb_words=4)
        author = fake.name()
        daily_fee = str(
            fake.pydecimal(min_value=0.00, max_value=9.00, right_digits=2)
        )
        book = {
            "model": "books.book",
            "pk": pk,
            "fields": {
                "title": title,
                "author": author,
                "cover": random.choice(["HARD", "SOFT"]),
                "inventory": random.randint(0, 10),
                "daily_fee": daily_fee,
            },
        }

        books_data.append(book)
    return books_data


def generator_fake_borrowing_data_for_db() -> list:
    borrowed_books = []
    for i in range(1000):
        pk = i + 30
        user_id = random.randint(30, 130)
        book_id = random.randint(30, 1130)
        borrowed_book = {
            "model": "borrowing.borrowing",
            "pk": pk,
            "fields": {
                "borrow_date": str(
                    fake.date_between(start_date="-1y", end_date="today")
                ),
                "expected_return_date": str(
                    fake.date_between(start_date="today", end_date="+1y")
                ),
                "actual_return_date": str(
                    fake.date_between(start_date="today", end_date="+1y")
                ),
                "user_id": user_id,
                "book_id": book_id,
            },
        }
        borrowed_books.append(borrowed_book)
    return borrowed_books


def data_fusion(*args, **kwargs) -> list:
    """
    Make a fusion lists to 1 list.
    """
    new_data = []
    for arg in args:
        new_data.extend(arg)
    new_data = []
    for arg in args:
        new_data.extend(arg)

    return new_data


def save_users_data_to_json(data: list, file_name: str) -> None:
    """
    Save a list of user data to a JSON file.
    """
    with open(f"{file_name}.json", "w") as file:
        json.dump(data, file, indent=4)


def open_json_file(file_name: str) -> list:
    """
    Open a JSON file and return its contents as a list of dictionaries.
    """
    with open(file_name, "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    users = generate_fake_user_data()
    books = generate_fake_books_data_for_db()
    borrowed = generator_fake_borrowing_data_for_db()

    data_for_json = data_fusion(users, books, borrowed)

    save_users_data_to_json(data_for_json, "example_data_for_db")
