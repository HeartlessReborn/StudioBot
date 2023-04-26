import psycopg2
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read("settings.cfg")

class Database:
    def __init__(self):
        self.connect = psycopg2.connect(
            host=cfg.get("Database", "host"),
            database=cfg.get("Database","database"),
            user=cfg.get("Database","user"),
            password=cfg.get("Database","password")
        )
        self.connect.autocommit = True
        self.connect.set_client_encoding("UTF8")
        self.cursor = self.connect.cursor()

    def CreateTables(self):
        with self.connect:
            users = self.cursor.execute("""create table if not exists users(
            id bigint,
            ban bigint
            )""")
            tasks = self.cursor.execute("""create table if not exists tasks(
            id serial PRIMARY KEY,
            text text,
            executor bigint
            )""")
            return users, tasks

    def add_user(self,id_):
        with self.connect:
            return self.cursor.execute("insert into users values(%s, 0)",(id_,))

    def user_exists(self, id_):
        with self.connect:
            self.cursor.execute("select id from users where id = %s",(id_,))
            a: bool = bool(len(self.cursor.fetchmany(1)))
            return a

    def create_task(self, text: str):
        with self.connect:
            self.cursor.execute("insert into tasks(text) values(%s)",(text,))
            self.cursor.execute("select id from tasks where text = %s",(text,))
            return self.cursor.fetchone()

    def edit_executor(self, id_, username):
        print(id_,username)
        with self.connect:
            self.cursor.execute("UPDATE tasks SET executor = {} WHERE id = {};".format(username,id_))
            return True


