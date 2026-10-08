import shutil
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_PATH = BASE_DIR / "database" / "hospital.db"
BACKUP_DIR = BASE_DIR / "backups"


def create_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    if not DATABASE_PATH.exists():
        raise FileNotFoundError("Database file not found.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_name = f"hospital_backup_{timestamp}.db"
    backup_path = BACKUP_DIR / backup_name

    shutil.copy2(DATABASE_PATH, backup_path)

    return backup_path


def get_backups():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    backups = sorted(
        BACKUP_DIR.glob("hospital_backup_*.db"),
        reverse=True,
    )

    return backups


def restore_backup(backup_path):
    backup_path = Path(backup_path)

    if not backup_path.exists():
        raise FileNotFoundError("Backup file not found.")

    if not DATABASE_PATH.exists():
        raise FileNotFoundError("Database file not found.")

    shutil.copy2(backup_path, DATABASE_PATH)

    return True