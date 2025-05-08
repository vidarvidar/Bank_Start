# has accounts
# can apply for an account
# can borrow
# can ask for credit
# can try update personal info
from account import Account


class Customer:
    accounts = []

    def __init__(self, name, ssn): # konstruktor
        self.name = name
        self.ssn = ssn

    def add_account(self, bank, type):
        new_account = Account(bank, "Personal_Account", self.ssn)
        self.accounts.append(new_account)
        return new_account