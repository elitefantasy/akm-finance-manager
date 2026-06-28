import os
import shutil

from core.database import DatabaseManager

from kivy.app import App




def backup_database(source_path, database_name, backup_dir=None):
    if backup_dir is None:
        backup_dir = os.path.join(
            App.get_running_app().user_data_dir,
            "backups",
        )

    os.makedirs(backup_dir, exist_ok=True)

    destination = os.path.join(
        backup_dir,
        database_name,
    )

    shutil.copy2(source_path, destination)

    return destination


def import_database_file(
    filename,
    user_data_dir,
    backup_dir=None,):

    if backup_dir is None:
        backup_dir = os.path.join(
            App.get_running_app().user_data_dir,
            "backups",
        )

    db_name = normalize_database_filename(filename)

    source = os.path.join(
        backup_dir,
        db_name,
    )

    destination = os.path.join(
        user_data_dir,
        db_name,
    )

    if not os.path.exists(source):
        return False, "Database not found", db_name

    if os.path.exists(destination):
        return False, "Database already exists", db_name

    is_valid, error_message = (
        DatabaseManager.validate_database_schema(source)
    )

    if not is_valid:
        return False, error_message, db_name

    shutil.copy2(source, destination)

    return True, "", db_name




def list_backup_databases(backup_dir=None):
    if backup_dir is None:
        backup_dir = os.path.join(
            App.get_running_app().user_data_dir,
            "backups",
        )

    if not os.path.exists(backup_dir):
        return []

    return sorted(
        filename
        for filename in os.listdir(backup_dir)
        if filename.endswith(".db")
    )
