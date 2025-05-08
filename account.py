# can withdraw
# can deposit
# has interest
# has balance
# has currency

class Account:

    def __init__(self, bank, type, nr):
        self.bank = bank
        self.type = type
        self.nr = bank.banknr + "-" +  nr
        self.balance = 0
        self.credit = 0

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

