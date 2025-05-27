# can withdraw
# can deposit
# has interest
# has balance
# has currency
import random

from db_deprecated import Db
from transaction_deprecated import Transaction


class Account:

    def __init__(self):
        self.conn = Db().get_conn()
        self.balance = 0

    @staticmethod
    def generate_nr():
        return str(random.randint(10 ** 9, 10 ** 10 - 1))

    def create(self, customer, bank, type, nr):
        customer = customer.id
        type = type
        nr = bank.banknr + "-" + nr
        bank = bank.id
        credit = 0

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO accounts (customer, bank, type, nr, credit) VALUES (%s, %s, %s, %s, %s)", [customer, bank, type, nr, credit])
                self.conn.commit()
                print(f"Account '{nr}' created successfully. Getting data.")
        except:
            print(f"[Warning] Account with number {nr} already exists. Getting data.")
        return self.get(nr)

    def get(self, nr):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE nr = %s", [nr])
        account = cursor.fetchone()
        if(account[0]):
            print(f"Customer loaded.")
            self.id = account[0]
            self.customer = account[1]
            self.bank = account[2]
            self.type = account[3]
            self.nr = account[4]
            self.credit = account[5]
            self.transactions = self.get_transactions()
            return self
        else:
            print(f"[Warning] Account {nr} not found.")
            return None

    def get_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE account_nr = %s", [self.nr,])
        transactions = cursor.fetchall()
        ts = []
        for transaction in transactions:
            ts.append({
                "id": transaction[0],
                "amount": transaction[1],
                "account": transaction[2]
            })
        return ts

    def get_balance(self):
        balance = 0
        for transaction in self.get_transactions():
            balance += transaction['amount']
        self.balance = balance
        return balance

    def deposit(self, amount):
        if amount > 0:
            Transaction().create(amount, self)

    def withdraw(self, amount):
        if(amount <= self.get_balance() + self.credit):
            Transaction().create(-amount, self)
            return -amount
        else:
            return 0

