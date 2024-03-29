import sqlite3

class Database:
        def __init__ (self):
                # open connection to the database
                self.connector = sqlite3.connect ("database.db")
                self.cursor = self.connector.cursor ()

        def execute (self, sql_query):
                # execute the query and save changes
                self.cursor.execute (sql_query)
                self.connector.commit ()

        def close_connection (self):
                # save the changes and commit 
                self.connector.commit ()
                self.cursor.close ()
                self.connector.close ()

        def append_message (self, username, message):
                sql_query = f"""INSERT INTO 
                                                CHAT 
                                                VALUES ('{username}', '{message}');"""                                          
                self.execute (sql_query)

def create_database ():
        database = Database ()

        # query to create the table
        database.execute ("""CREATE TABLE IF NOT EXISTS AUTH (
                        Username VARCHAR (255) NOT NULL UNIQUE,
                        Password VARCHAR (255) NOT NULL
                );
                """)
        # Create the chat table
        database.execute ("""CREATE TABLE IF NOT EXISTS CHAT (
                        Username VARCHAR (255) NOT NULL,
                        Message TEXT NOT NULL
                );
                """)

        # commit the changes
        database.close_connection ()


if __name__ == "__main__":
        create_database ()
