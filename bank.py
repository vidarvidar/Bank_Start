# has accounts
# has customers
# can lend (from its own accounts)
# can transfer (to/from other banks)

class Bank:
    customers = []
    accounts = []

    def __init__(self, name, banknr):
        self.name = name
        self.banknr = banknr

    def add_customer(self, customer):
        new_account = customer.add_account(self, "Personal_account")
        self.accounts.append(new_account)
        self.customers.append(customer)
