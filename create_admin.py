
import getpass
import sqlite3

from app.database.db import initialize_database
from app.services.user_service import create_user


def main():
    initialize_database()

    username = input("Admin username: ").strip()

    if len(username) < 3:
        print("Username must contain at least 3 characters.")
        return

    password = getpass.getpass("Admin password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    if len(password) < 12:
        print("Use a password with at least 12 characters.")
        return

    try:
        user_id = create_user({
            "username": username,
            "password": password,
            "role": "Admin",
        })

        print(f"Administrator created successfully. ID: {user_id}")

    except sqlite3.IntegrityError:
        print("Username already exists.")


if __name__ == "__main__":
    main()
