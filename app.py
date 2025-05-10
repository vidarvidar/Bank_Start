# starta bank (banktjänsterna)
from bank import Bank
from customer import Customer
from db import Db

def main():
    setupExample()
    # usageExample()

def setupExample():
    # create a new bank
    bank = Bank().create("Tres Banko", "2345") # return bank object
    # create a new customer
    customer = Customer().create("Benjamin", "197001092456") # return customer object
    # add the customer to the bank we created (and add a personal account, which every new customer gets)
    bank.add_customer(customer)

def usageExample():
    customer = Customer().get("197001092456")
    my_account = customer.accounts[0]
    my_account.deposit(1000)
    print(my_account.get_balance())
    my_account.withdraw(300)
    print(my_account.get_balance())
    my_account.withdraw(900)
    print(my_account.get_balance())


if __name__ == '__main__':
    main()