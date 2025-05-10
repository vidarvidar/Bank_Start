# has accounts
# has customers
# can lend (from its own accounts)
# can transfer (to/from other banks)

from account import Account
from db import Db

class Bank:
    customers = []
    accounts = []

    def __init__(self):
        self.conn = Db().get_conn()

    def create(self, name, banknr):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO banks (name, banknr) VALUES (%s, %s)", [name, banknr])
                self.conn.commit()
                print(f"Bank '{name}' created successfully. Getting data.")
        except:
            print(f"[Warning] Bank with name {name} already exists. Getting data.")
        return self.get(banknr)

    def get(self, banknr):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM banks WHERE banknr = %s", [banknr])
        bank = cursor.fetchone()
        if(bank[0]):
            print(f"Bank loaded.")
            self.id = bank[0]
            self.name = bank[1]
            self.banknr = bank[2]
            return self
        else:
            print(f"[Warning] Bank with banknr {banknr} not found.")
            return None

    def add_customer(self, customer):
        new_account = Account().create(customer, self, "Personal_account", customer.ssn)
        self.accounts.append(new_account)
        self.customers.append(customer)

    def add_account(self, bank, type):
        new_account = Account(bank, "Personal_Account", self.ssn)
        self.accounts.append(new_account)
        return new_account