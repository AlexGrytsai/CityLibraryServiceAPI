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


if __name__ == "__main__":
    users = generate_fake_user_data()
