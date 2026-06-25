import sqlite3
import os
from kivy.app import App

DEFAULT_DB = "finance.db"

class DatabaseManager:

    def __init__(self, db_name=DEFAULT_DB):
        self.db_name= db_name
        
        self.db_path = os.path.join(
            App.get_running_app().user_data_dir, db_name
        )

        self.conn = sqlite3.connect(self.db_path)

        print(self.db_path)

    def create_database(self):

        cursor = self.conn.cursor()
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            note TEXT,
            date TEXT
        )
        """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            day INTEGER,
            last_added TEXT
        )
        """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_date
        ON transactions(date)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_category
        ON transactions(category)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_transactions_type
        ON transactions(type)
        """)
    
        default_categories = [
            "Food",
            "Travel",
            "Shopping",
            "Medical",
            "Education",
            "Other"
        ]
    
        for category in default_categories:
    
            cursor.execute(
                """
                INSERT OR IGNORE INTO categories(name)
                VALUES(?)
                """,
                (category,)
            )
    
        self.conn.commit()
        
    
    def execute_query(self,query,params=()):

        cursor = self.conn.cursor()

        cursor.execute(query,params)

        self.conn.commit()

        
    
    def fetch_query(self,query,params=()):

        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        cursor.execute(query,params)

        rows = [
            dict(row)
            for row in cursor.fetchall()
        ]

        

        return rows
    
    def load_transactions_db(self):

        return self.fetch_query(

            """
            SELECT *
            FROM transactions
            """

        )
    
    
    def save_transaction_db(self,transaction):
        # get column names
        columns = ", ".join(transaction.keys())   
        
        # create placefolder, len gives nof fields dict has eg:5, then ["?"] * 5  becomes ['?', '?', '?', '?', '?'], join makes "?, ?, ?, ?, ?"
        placeholders = ", ".join(["?"] * len(transaction))

        values = tuple(transaction.values())

        cursor = self.conn.cursor()

        cursor.execute(

            f"""
            INSERT INTO transactions
            ({columns})
            VALUES
            ({placeholders})
            """,

            values
        )

        self.conn.commit()

        return cursor.lastrowid
    
    def   delete_transaction_db(self,transaction_id):
        self.execute_query(
            """
            DELETE FROM transactions
            WHERE id=?
            """,
            (transaction_id,)
        )    
    
    def update_transaction_db(self,transaction_id,data):
        columns=", ".join(
            f"{key}=?"
            for key in data.keys()
        )
        
        values = list(data.values())
        
        values.append(transaction_id)
        
        self.execute_query(
            f"""
            UPDATE transactions
            SET {columns}
            WHERE id=?
            """,
            
            tuple(values)
        )
    
    def clear_transactions_db(self):
        self.execute_query(
            """
            DELETE FROM transactions
            """
        )
    
    def load_recurring_db(self):
        return self.fetch_query(
            """
            SELECT *
            FROM recurring_transactions
            """
        )
        
    
    def save_recurring_db(self,recurring):
        columns = ", ".join(
            recurring.keys()
        )
        placeholders = ", ".join(
            ["?"] * len(recurring)
        )
        values = tuple(
            recurring.values()
        )
        self.execute_query(
            f"""
            INSERT INTO recurring_transactions
            ({columns})
            VALUES
            ({placeholders})
            """,
            values
        )
    
    def delete_recurring_db(self,recurring_id):
        self.execute_query(
            """
            DELETE FROM recurring_transactions
            WHERE id=?
            """,
            (recurring_id,)
        )
    
    def update_recurring_db(self,recurring_id,data):
        columns = ", ".join(
            f"{key}=?"
            for key in data.keys()
        )
        values = list(
            data.values()
        )
        values.append(
            recurring_id
        )
        self.execute_query(
            f"""
            UPDATE recurring_transactions
            SET {columns}
            WHERE id=?
            """,
            tuple(values)
        )
    
    
    
    def load_categories_db(self):

        rows = self.fetch_query(
            """
            SELECT name
            FROM categories
            ORDER BY name
            """
        )

        return[
            row["name"]
            
            for row in rows
        ]
    
    def save_category_db(self, name):
        self.execute_query(
            """
            INSERT INTO categories(name)
            VALUES(?)
            """,
            (name,)
        )
        
    def delete_category_db(self, category_id):
        self.execute_query(
            """
            DELETE FROM categories
            WHERE id=?
            """,
            (category_id,)
        )
    
    def update_category_db(self,category_id,name):
        self.execute_query(

            """
            UPDATE categories
            SET name=?
            WHERE id=?
            """,
            (
                name,
                category_id
            )
        )
