import psycopg2 as db
from main.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import random


class Database:
    def __init__(self):
        self.connect = db.connect(
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        user_table = """
        CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL)"""

        movies_table = """
        CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        movie_name VARCHAR(50),
        language VARCHAR(20),
        quality VARCHAR(10),
        janri VARCHAR(50),
        movie_id BIGINT,
        create_date TIMESTAMP DEFAULT now());"""

        dowunload_table = """
        CREATED TABLE IF NOT EXISTS download (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id),
        id INT REFERENCES movies(id),
        create_date TIMESTAMP DEFAULT now());"""

        self.cursor.execute(user_table)
        self.cursor.execute(movies_table)
        self.cursor.execute(dowunload_table)

        self.connect.commit()
