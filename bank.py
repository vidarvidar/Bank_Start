# has accounts
# has customers
# can lend (from its own accounts)
# can transfer (to/from other banks)

class Bank:
    customers = []
    accounts = []

    def __init__(self, name, banknr, db_conn):
        self.name = name
        self.banknr = banknr
        self.conn = db_conn
        self.sync()

    def add_customer(self, customer):
        new_account = customer.add_account(self, "Personal_account")
        self.accounts.append(new_account)
        self.customers.append(customer)

    # checks if there already is a bank of this name, if there isn't it is created
    def sync(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM banks WHERE name = %s AND banknr = %s", [self.name, self.banknr])
        bank = cursor.fetchone()
        if(bank is None):
            cursor.execute("INSERT INTO banks (name, banknr) VALUES (%s, %s)",[self.name, self.banknr])
            self.conn.commit()
