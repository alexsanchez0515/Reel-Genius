import bcrypt
import sqlite3
from os import PathLike
from pathlib import Path


class LoginDB:
    def __init__(self, db_path: Path | str = "login.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        # Create table to self.path if table does not exist already
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL
                password TEXT NOT NULL           
            )
        ''')
        self.conn.commit()

    def add_user(self, email: str, password: str):
        # Insert new user to database
        try:
            self.cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Error: Account with this email already exists.")

    def get_user(self, email: str):
        # Retrieve user from database
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def delete_user(self, email: str):
        # Delete a user from database
        self.cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        self.conn.commit()

    def __del__(self):
        # Close connection when db is closed
        self.cursor.close()
        self.conn.close()


class LoginAuthUtil:
    def __init__(self):
        self.salt = bcrypt.gensalt()

    def hash(self, pw: str):
        bytes = pw.encode('utf-8')
        hashed_pw = bcrypt.hashpw(password=bytes, salt=self.salt)
        return hashed_pw


if __name__ == "__main__":
    login = LoginAuthUtil()
    password = "R33s5jnm!!"
    other_password = "R33s5jnm!"

    new_password = login.hash(pw=password)
    other_password = login.hash(pw=other_password)
    print(f"{new_password}")
    print(f"{other_password}")
