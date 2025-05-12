from db import Db

class Transaction:

    def __init__(self):
        self.conn = Db().get_conn()

    def create(self, amount, account):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO transactions (amount, account_nr) VALUES (%s, %s)", [amount, account.nr])
                self.conn.commit()
                print(f"Transaction '{amount}' created successfully.")
        except:
            print(f"[Warning] Transaction blocked due to constraint violation, date or non approved customer.")
        return amount
