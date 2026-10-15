
from getpass import getpass

from app.database.db import initialize_database
from app.services.user_service import create_user

def main():
    initialize_database()

    username = input("Admin username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    password = getpass("Admin password (minimum 8 characters): ")
    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return

    confirm = getpass("Confirm password: ")
    if password != confirm:
        print("Passwords do not match.")
        return

    try:
        user_id = create_user({
            "username": username,
            "password": password,
            "role": "Admin",
            "is_active": 1,
        })
        print(f"Admin account created successfully. User ID: {user_id}")
    except Exception as exc:
        print(f"Could not create admin account: {exc}")

if __name__ == "__main__":
    main()
