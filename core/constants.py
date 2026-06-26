import os


APP_NAME = "FinanceManager"
DEFAULT_DB = "finance.db"
SETTINGS_FILE = "settings.json"

DOWNLOAD_FOLDER_NAME = "Download"
BACKUP_FOLDER_NAME = APP_NAME
BACKUP_DIR_FALLBACK = "/storage/emulated/0/Download/FinanceManager"

EXPORTS_DIR_NAME = "exports"
BACKUPS_DIR_NAME = "backups"
LOGS_DIR_NAME = "logs"
CSV_EXPORT_FILE = "finance_export.csv"

DEFAULT_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Medical",
    "Education",
    "Other",
]

REQUIRED_SCHEMA = {
    "transactions": {
        "id": "INTEGER",
        "type": "TEXT",
        "amount": "REAL",
        "category": "TEXT",
        "note": "TEXT",
        "date": "TEXT",
    },
    "recurring_transactions": {
        "id": "INTEGER",
        "amount": "REAL",
        "category": "TEXT",
        "day": "INTEGER",
        "last_added": "TEXT",
    },
    "categories": {
        "id": "INTEGER",
        "name": "TEXT",
    },
}


def get_backup_dir():
    try:
        from android.storage import primary_external_storage_path

        return os.path.join(
            primary_external_storage_path(),
            DOWNLOAD_FOLDER_NAME,
            BACKUP_FOLDER_NAME
        )
    except Exception:
        return BACKUP_DIR_FALLBACK
