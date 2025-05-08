# starta bank (banktjänsterna)
from bank import Bank
from customer import Customer


def main():
    bank = Bank("Banko", "1234") # name, banknr
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