from cgitb import reset
from datetime import datetime
from os.path import commonpath
import random
from . database import Database


class KinoDatabase(Database):
    def create_table_kino(self):
        sql="""
            CREATE TABLE IF NOT EXISTS Kino(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id VARCHAR(3000) NOT NULL,
                caption TEXT NULL,
                name TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
                );
            """
        self.execute(sql,commit=True)

    def add_movie(self, post_id: int, file_id: str,name:str, caption: str = None, created_at: str = None, updated_at: str = None):
        if self.get_movie_by_post_id(post_id):
            raise ValueError(f"post_id {post_id} already exists in the database.")

        sql = """
            INSERT INTO Kino (post_id, file_id, name, caption, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        timestamp = datetime.now().isoformat()
        created_at = created_at or timestamp
        updated_at = updated_at or timestamp
        self.execute(sql, parameters=(post_id, file_id, name,caption, created_at, updated_at), commit=True)

    def generate_unique_post_id(self):
        while True:
            post_id = random.randint(1, 1000)  # Random number between 1 and 2^31-1
            if not self.get_movie_by_post_id(post_id):  # Ensure it's unique
                return post_id



    def update_kino_caption(self,new_caption:str,post_id:int):
        sql="""
            UPDATE Kino
            SET caption = ?,updated_at = ?
            WHERE post_id = ?
            """
        updated_time=datetime.now().isoformat()
        self.execute(sql,parameters=(new_caption,updated_time,post_id),commit=True)

    def get_movie_by_post_id(self, post_id: int):
        sql = """
            SELECT file_id, caption FROM Kino
            WHERE post_id=?
        """
        result = self.execute(sql, parameters=(post_id,), fetchone=True)
        if result:
            return {
                'file_id': result[0],
                'caption': result[1]
            }
        return None
    def get_movie_cap_by_id(self,post_id: int):
        sql="""
            SELECT caption FROM Kino
            WHERE post_id = ?
            """
        result=self.execute(sql,parameters=(post_id,),fetchone=True)
        if result:
            return result[0]

        return None
    def get_movie_by_name(self,name_of:str):
        sql="""
            SELECT file_id, caption, name FROM Kino
            WHERE name=?
            """
        result=self.execute(sql,parameters=(name_of,),fetchone=True)
        if result:
            return {
                'file_id': result[0],
                'caption': result[1],
                'nameo':result[2]
            }
        return None

    def delete_movie(self,post_id:int):
        sql="""
            DELETE FROM Kino WHERE post_id = ?
            """
        self.execute(sql,parameters=(post_id,),commit=True)

    def count_kino(self):
        sql = """
            SELECT COUNT(*) FROM Kino
        """
        return self.execute(sql, fetchone=True)  # Returns a single tuple (count,)

    def add_column(self):
        sql="""
            ALTER TABLE Kino
            ADD name TEXT NOT NULL
            """
        self.execute(sql,commit=True)

    def get_movies_bugun(self):
        sql = """
            SELECT name FROM Kino
            WHERE DATE(created_at) = DATE('now')
        """
        return self.execute(sql, fetchall=True)

    def get_movies_hafta(self):
        sql = """
            SELECT name FROM Kino
            WHERE DATE(created_at) >= DATE('now', '-7 days')
        """
        return self.execute(sql, fetchall=True)

    def get_movies_oy(self):
        sql = """
            SELECT name FROM Kino
            WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
        """
        return self.execute(sql, fetchall=True)