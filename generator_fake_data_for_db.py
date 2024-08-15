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
    for i in range(10):
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
                "daily_fee": daily_fee
            },
        }

        books_data.append(book)
    return books_data


def data_fusion(*args, **kwargs) -> list:
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

    data_for_json = data_fusion(users, books)

    save_users_data_to_json(data_for_json, "example_data_for_db")
