import psycopg2

class Db:

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='pythonbank',
            user='postgres',
            password='root',
            host='localhost',
            port='5432'
        )

    def get_conn(self):
        return self.conn