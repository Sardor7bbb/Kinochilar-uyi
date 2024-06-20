import psycopg2 as db
from main.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
import re


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
        chat_id BIGINT NOT NULL,
        create_date TIMESTAMP DEFAULT now());"""

        movies_table = """
        CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        movie_name VARCHAR(50),
        language VARCHAR(20),
        quality VARCHAR(10),
        genre VARCHAR(50),
        movie_id VARCHAR(200) NOT NULL,
        instagram_link VARCHAR(30) NULL,
        youtube_link VARCHAR(30) NULL,
        create_date TIMESTAMP DEFAULT now());"""

        download_table = """
        CREATE TABLE IF NOT EXISTS download (
        download_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id),
        id INT REFERENCES movies(id),
        create_date TIMESTAMP DEFAULT now());"""

        self.cursor.execute(user_table)
        self.cursor.execute(movies_table)
        self.cursor.execute(download_table)

        self.connect.commit()

    def get_add_movies(self, data: dict):
        movie_name = data["movie_name"]
        language = data["language"]
        quality = data["quality"]
        genre = data["genre"]
        movie_id = data["movie_id"]
        query = f"""INSERT INTO movies (movie_name, language, quality, genre, movie_id) VALUES ('{movie_name}','{language}','{quality}','{genre}','{movie_id}')"""
        self.cursor.execute(query)
        self.connect.commit()
        return True

    def get_new_user_id(self, user_id):
        query = f"""INSERT INTO users (chat_id) VALUES ({user_id})"""
        self.cursor.execute(query)
        self.connect.commit()
        return True

    def get_instagram_link(self):
        query = f"""SELECT * FROM movies WHERE instagram_link IS NULL OR instagram_link = ''"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def movies(self):
        query = f"""SELECT * FROM movies"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_user_chat_id(self, chat_id):
        query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def movies_id(self, kino_id):
        query = f"""SELECT * FROM movies WHERE id = '{kino_id}'"""
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def add_instagram_link(self, link, kino_id):
        query = f""" UPDATE movies SET instagram_link = '{link}' WHERE id = {kino_id}"""
        self.cursor.execute(query)
        self.connect.commit()
        return True

    def search_movies(self, link):
        query = f"""SELECT * FROM movies WHERE instagram_link = '{link}' """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def user_downloader(self, user_id, movie_id):
        query = f"""INSERT INTO download (user_id, id) VALUES ({user_id}, {movie_id})"""
        self.cursor.execute(query)
        self.connect.commit()
        return True

    def get_user_downloads(self, user_id, movie_id):
        query = f""" 
        SELECT 
            users.user_id, 
            movies.id 
        FROM 
            users, movies, download
        WHERE 
            download.user_id = users.user_id 
            AND download.id = movies.id 
            AND users.user_id = {user_id}
            AND movies.id = {movie_id}
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def get_about(self):
        query = """
        SELECT 'users' as table_name, COUNT(*) as count FROM users
            UNION ALL
        SELECT 'movies', COUNT(*) FROM movies
            UNION ALL
        SELECT 'download', COUNT(*) FROM download;
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
