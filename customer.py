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
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO customers (name, ssn) VALUES (%s, %s)",[name, ssn])
                self.conn.commit()
                print(f"Customer '{name}' created successfully. Getting data.")
        except:
            print(f"[Warning] Customer {name} already exists. Getting data.")
        return self.get(ssn)

    def get(self, ssn):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE ssn = %s", [ssn])
        customer = cursor.fetchone()
        if(customer[0]):
            print(f"Customer loaded.")
            self.id = customer[0]
            self.name = customer[1]
            self.ssn = customer[2]
            self.accounts = self.get_accounts()
            return self
        else:
            print(f"[Warning] Customer with ssn {ssn} not found.")
            return None

    def get_accounts(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE customer = %s", [self.id,])
        accounts = cursor.fetchall()
        accs = []
        for account in accounts:
            accs.append(Account().get(account[4]))
        return accs

    def old_get_accounts(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE customer = %s", [self.id,])
        accounts = cursor.fetchall()
        accs = []
        for account in accounts:
            accs.append({
                "id": account[0],
                "customer": account[1],
                "bank": account[2],
                "type": account[3],
                "nr": account[4],
                "credit": account[5]
            })
        return accs

