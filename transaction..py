from db import Db

class Transaction:

    def __init__(self):
        self.conn = Db().get_conn()

    def create(self, account, amount):
        account = account.nr
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO transactions (account, amount) VALUES (%s, %s)", [account, amount])
                self.conn.commit()
                print(f"Transaction '{amount}' created successfully.")
        except:
            print(f"[Warning] This should not happen.")
        return amount

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

