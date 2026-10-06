import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# SQLite database location
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "hospital.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    """Create all required database tables if they do not already exist."""

    connection = get_connection()

    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                blood_group TEXT,
                phone TEXT,
                address TEXT,
                emergency_contact TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                department TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            );

            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                diagnosis TEXT NOT NULL,
                prescription TEXT,
                notes TEXT,
                record_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            );

            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_status TEXT NOT NULL DEFAULT 'Pending',
                bill_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            );

            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                module TEXT NOT NULL,
                record_id INTEGER,
                description TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
        )

        connection.commit()

    finally:
        connection.close()