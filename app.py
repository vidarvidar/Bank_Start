# starta bank (banktjänsterna)
from bank import Bank
from customer import Customer
from db import Db

def main():
    db = Db()
    conn = db.get_conn()
    bank = Bank("Banko", "1234", conn) # name, banknr
    customer = Customer("Benjamin", "197001092456") # new Customer
    bank.add_customer(customer)
    my_account = customer.accounts[0]
    my_account.deposit(1000)
    print(my_account.get_balance())
    my_account.withdraw(300)
    print(my_account.get_balance())
    my_account.withdraw(900)
    print(my_account.get_balance())


if __name__ == '__main__':
    main()