import json
import os

from database import DatabaseManager


def create_database(name):
    db_name = normalize_database_name(name)

    temp_db = DatabaseManager(db_name)
    temp_db.create_database()
    temp_db.conn.close()

    return db_name


def list_databases(user_data_dir):
    return sorted(
        filename for filename in os.listdir(user_data_dir)
        if filename.endswith(".db")
    )


def save_selected_database(user_data_dir, db_name):
    settings_path = os.path.join(user_data_dir, "settings.json")

    with open(settings_path, "w") as settings_file:
        json.dump({"database": db_name}, settings_file)


def rename_database_file(
    user_data_dir,
    old_name,
    new_name,
    current_database
):
    db_name = normalize_database_name(new_name)

    old_path = os.path.join(user_data_dir, old_name)
    new_path = os.path.join(user_data_dir, db_name)

    if os.path.exists(new_path):
        return False, "Database already exists", db_name

    os.rename(old_path, new_path)

    if current_database == old_name:
        save_selected_database(user_data_dir, db_name)

    return True, "", db_name


def delete_database_file(user_data_dir, db_name, current_database):
    if db_name == current_database:
        return False, "Cannot delete active database"

    db_path = os.path.join(user_data_dir, db_name)

    os.remove(db_path)

    return True, ""


def normalize_database_name(name):
    db_name = name.strip()

    if not db_name:
        raise ValueError("Enter database name")

    if not db_name.endswith(".db"):
        db_name += ".db"

    return db_name
