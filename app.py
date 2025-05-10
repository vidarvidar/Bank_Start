# starta bank (banktjänsterna)
from bank import Bank
from customer import Customer
from db import Db

def main():
    setupExample()
    usageExample()

def setupExample():
    # create a new bank
    bank = Bank().create("Tres Banko", "2345") # return bank object
    # create a new customer
    customer = Customer().create("Benjamin", "197001092456") # return customer object
    # add the customer to the bank we created (and add a personal account, which every new customer gets)
    bank.add_customer(customer)

def usageExample():
    bank = Bank().get("2345")
    customer1 = Customer().get("197001092456")
    print("customer1 " + customer1.name)
    for account in customer1.accounts:
        print(account['nr'])
    # print("customer1 account[0] " + customer1.accounts[0].nr)
    # customer2 = bank.get_customer("197001092456")
    # print("customer2 " + customer2.name)
    # print("customer2 account[0] " + customer2.accounts[0].nr)

def laters():
    my_account = customer.accounts[0]
    my_account.deposit(1000)
    print(my_account.get_balance())
    my_account.withdraw(300)
    print(my_account.get_balance())
    my_account.withdraw(900)
    print(my_account.get_balance())


if __name__ == '__main__':
    main()