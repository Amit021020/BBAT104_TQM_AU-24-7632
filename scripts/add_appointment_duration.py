
from app.database.db import get_connection


def migrate():
    connection = get_connection()

    try:
        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(appointments)"
            ).fetchall()
        }

        if "duration_minutes" not in columns:
            connection.execute(
                """
                ALTER TABLE appointments
                ADD COLUMN duration_minutes
                INTEGER NOT NULL DEFAULT 30
                CHECK (duration_minutes IN (30, 60))
                """
            )

            connection.commit()
            print("Added duration_minutes column.")
        else:
            print("Duration column already exists.")

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
