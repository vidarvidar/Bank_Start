# has accounts
# can apply for an account
# can borrow
# can ask for credit
# can try update personal info

from account import Account
from db import Db


class Customer:
    accounts = []

    def __init__(self): # konstruktor
        self.conn = Db().get_conn()

    def create(self, name, ssn):
        self.name = name
        self.ssn = ssn
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO customers (name, ssn) VALUES (%s, %s)",[self.name, self.ssn])
                self.conn.commit()
                print(f"Customer '{self.name}' created successfully.")
        except:
            print(f"[Warning] Customer {self.name} already exists. Skipping creation.")
        return self

