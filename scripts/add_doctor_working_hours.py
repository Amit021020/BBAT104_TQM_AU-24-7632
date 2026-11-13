
from app.database.db import get_connection


def migrate():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS doctor_working_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL
                    CHECK (day_of_week BETWEEN 0 AND 6),
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
                    CHECK (is_active IN (0, 1)),
                UNIQUE (doctor_id, day_of_week),
                FOREIGN KEY (doctor_id)
                    REFERENCES doctors(id)
                    ON DELETE RESTRICT,
                CHECK (start_time < end_time)
            )
            """
        )

        connection.commit()
        print("Doctor working-hours table is ready.")

    finally:
        connection.close()


if __name__ == "__main__":
    migrate()
