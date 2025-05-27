# starta bank (banktjänsterna)
from old_files.bank_deprecated import Bank
from old_files.customer import Customer


# this is just usage examples of how to use the various methods in the bank.
def main():
    # create a new bank
    bank = Bank().create("Tres Banko", "2345") # return bank object
    # create a new customer
    customer = Customer().create("Bonjamin", "8001092456") # return customer object

    # add the customer to the bank we created (and add a personal account, which every new customer gets)
    bank.add_customer(customer)
    personal_account = customer.accounts[0]
    print(f"before personal dep {personal_account.get_balance()}")
    # make a deposit
    personal_account.deposit(200)
    print(f"after personal dep {personal_account.get_balance()}")
    # withdraw too much, should not change balance
    personal_account.withdraw(300)
    print(f"after personal overdraw attempt  {personal_account.get_balance()}")
    # withdraw half
    personal_account.withdraw(100)
    print(f"after personal withdraw half {personal_account.get_balance()}")
    # withdraw the outstanding balance (effectively zeroing the account)
    balance = personal_account.get_balance()
    personal_account.withdraw(balance)
    print(f"after personal withdraw outstanding {personal_account.get_balance()}")


    # also add a savings account
    # nr = Account.generate_nr() # 8064047892
    savings_account = bank.add_account(customer, "Savings_account", "8064047892")
    print(f"before savings dep {savings_account.get_balance()}")
    # make a deposit
    savings_account.deposit(300)
    print(f"after savings dep {savings_account.get_balance()}")
    # withdraw too much, should not change balance
    savings_account.withdraw(400)
    print(f"after savings overdraw attempt  {savings_account.get_balance()}")
    # withdraw a third
    savings_account.withdraw(100)
    print(f"after savings withdraw half {savings_account.get_balance()}")
    # withdraw the outstanding balance (effectively zeroing the account)
    balance = savings_account.get_balance()
    savings_account.withdraw(balance)
    print(f"after savings withdraw outstanding {savings_account.get_balance()}")


if __name__ == '__main__':
    main()