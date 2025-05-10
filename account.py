# can withdraw
# can deposit
# has interest
# has balance
# has currency

from db import Db

class Account:

    def __init__(self):
        self.conn = Db().get_conn()
        self.balance = 0

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
            return self
        else:
            print(f"[Warning] Account {nr} not found.")
            return None

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

