class TableCreator:

    def __init__(self, database):
        self.database = database

    def __create_auth_table_if_nonexisting(self):
        self.database.execute ("""CREATE TABLE IF NOT EXISTS AUTH (
                    Username VARCHAR (255) NOT NULL,
                    Password VARCHAR (255) NOT NULL,
                    Primary Key(Username)
            );
        """)

    def __create_global_table_if_nonexisting(self):
        self.database.execute ("""CREATE TABLE IF NOT EXISTS GLOBAL (
                    Username VARCHAR (255) not null,
                    Message TEXT NOT NULL
            );
        """)

    def __create_messages_table_if_nonexisting(self):
        self.database.execute("""CREATE TABLE IF NOT EXISTS MESSAGE (
                    MESSAGE_TEXT TEXT not null,
                    FROM_USR varchar(255) not null,
                    TO_USR varchar(255) not null,
                    foreign key(FROM_USR) references AUTH(Username),
                    foreign key(TO_USR) references AUTH(Username)
            );
        """)

    def create_table_structures(self):
        self.__create_auth_table_if_nonexisting()
        self.__create_global_table_if_nonexisting()
        self.__create_messages_table_if_nonexisting()

