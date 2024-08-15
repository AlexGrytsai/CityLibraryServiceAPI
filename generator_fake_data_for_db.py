import json

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
