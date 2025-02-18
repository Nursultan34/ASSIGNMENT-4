import random
import string
import re
from datetime import datetime

class User:
    def __init__(self, user_id, name, surname, birthday, email, password):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.birthday = birthday

    def get_details(self):
        return f"ID: {self.user_id}, Name: {self.name} {self.surname}, Email: {self.email}, Age: {self.get_age()}"

    def get_age(self):
        today = datetime.today()
        age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age

class UserService:
    users = {}

    @classmethod
    def add_user(cls, user):
        cls.users[user.user_id] = user

    @classmethod
    def find_user(cls, user_id):
        return cls.users.get(user_id, None)

    @classmethod
    def delete_user(cls, user_id):
        if user_id in cls.users:
            del cls.users[user_id]

    @classmethod
    def update_user(cls, user_id, **kwargs):
        user = cls.find_user(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

    @classmethod
    def get_number(cls):
        return len(cls.users)

class UserUtil:
    @staticmethod
    def generate_user_id():
        year_prefix = str(datetime.today().year)[-2:]
        random_digits = ''.join(random.choices(string.digits, k=7))
        return int(year_prefix + random_digits)

    @staticmethod
    def generate_password():
        characters = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.digits) +
            random.choice(string.punctuation)
        )
        remaining = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=5))
        password = list(characters + remaining)
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def is_strong_password(password):
        return (
            len(password) >= 8 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)
        )

    @staticmethod
    def generate_email(name, surname, domain):
        return f"{name.lower()}.{surname.lower()}@{domain}"

    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

if __name__ == "__main__":
    try:
        print("User registration")
        name = input("Enter first name: ") or "John"
        surname = input("Enter last name: ") or "Doe"

        while True:
            try:
                birth_year = int(input("Enter birth year (YYYY): ") or 2000)
                birth_month = int(input("Enter birth month (MM): ") or 1)
                birth_day = int(input("Enter birth day (DD): ") or 1)
                birthday = datetime(birth_year, birth_month, birth_day)
                break
            except ValueError:
                print("Invalid date! Please enter a valid birth year, month, and day.")

        domain = input("Enter email domain (e.g., example.com): ") or "example.com"
        user_id = UserUtil.generate_user_id()
        email = UserUtil.generate_email(name, surname, domain)
        password = UserUtil.generate_password()

        user = User(user_id, name, surname, birthday, email, password)
        UserService.add_user(user)

        print("\nUser Created Successfully!")
        print(user.get_details())

        found_user = UserService.find_user(user.user_id)
        print("User found:" if found_user else "User not found")

        print(f"Total users: {UserService.get_number()}")
    except Exception as e:
        print(f"An error occurred: {e}")
