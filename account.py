# can withdraw
# can deposit
# has interest
# has balance
# has currency

from db import Db

class Account:

    def __init__(self):
        self.conn = Db().get_conn()

    def create(self, customer, bank, type, nr):
        self.customer = customer.id
        self.bank = bank.id
        self.type = type
        self.nr = bank.banknr + "-" + nr
        self.credit = 0
        self.balance = 0

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO accounts (customer, bank, type, nr, credit) VALUES (%s, %s, %s, %s, %s)", [self.customer, self.bank, self.type, self.nr, self.credit])
                self.conn.commit()
                print(f"Account '{self.name}' created successfully.")
        except:
            print(f"[Warning] Account with number {self.nr} already exists. Skipping creation.")
        return self

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if(amount <= self.balance + self.credit):
            self.balance -= amount
            return amount
        else:
            return 0

