import sqlite3
from components.table_creator import TableCreator


class Database:
    def __init__(self):
        self.connector = sqlite3.connect("database.db")
        self.cursor = self.connector.cursor()

    def execute(self, sql_query):
        self.cursor.execute(sql_query)
        self.connector.commit()

    def commit_and_close_connection(self):
        self.connector.commit()
        self.cursor.close()
        self.connector.close()

    def append_message_into_global(self, username, message):
        sql_query = f"""INSERT INTO
                        GLOBAL
                        VALUES ('{username}', '{message}');"""
        self.execute(sql_query)

    def create_user(self, username: str, password: str):
        query = f""" INSERT INTO AUTH (Username, Password)
                            VALUES ('{username}', '{password}'); """
        self.execute(query)


database = Database()
table_creator = TableCreator(database)

table_creator.create_table_structures()
database.commit_and_close_connection()
