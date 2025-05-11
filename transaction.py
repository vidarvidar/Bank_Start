from db import Db

class Transaction:

    def __init__(self):
        self.conn = Db().get_conn()

    def create(self, amount, account):
        account = account.id
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO transactions (amount, account) VALUES (%s, %s)", [amount, account])
                self.conn.commit()
                print(f"Transaction '{amount}' created successfully.")
        except:
            print(f"[Warning] This should not happen.")
        return amount
