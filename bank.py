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
        self.name = name
        self.banknr = banknr
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO banks (name, banknr) VALUES (%s, %s)", [self.name, self.banknr])
                self.conn.commit()
                print(f"Bank '{self.name}' created successfully.")
        except:
            print(f"[Warning] Bank with name {self.name} already exists. Skipping creation.")
        return self

    def add_customer(self, customer):
        new_account = Account().create(customer, self, "Personal_account", customer.ssn)
        self.accounts.append(new_account)
        self.customers.append(customer)

    def add_account(self, bank, type):
        new_account = Account(bank, "Personal_Account", self.ssn)
        self.accounts.append(new_account)
        return new_account