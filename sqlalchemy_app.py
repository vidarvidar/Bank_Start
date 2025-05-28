#app.py för sqlalchemy + ETL
import csv

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Customer, Account, Transaction
from db_sqlalchemy import init_db, engine
from etlfuncs import csv_reader_renamer, db_table_trasher, db_adder


def customer_account_main():

    db_table_trasher(Transaction)
    db_table_trasher(Account)
    db_table_trasher(Customer)
    init_db()
    db = Session(engine)

    # account_column_mapper = {'Customer': 'name', 'Address': 'address', 'Phone': 'phone', 'Personnummer': 'ssn',
    #                          'BankAccount': 'account_number'}
    # transaction_column_mapper = {'transaction_id': 'id', 'timestamp': 'timestamp', 'amount': 'amount',
    #                              'currency': 'currency', 'sender_account': 'sender_account',
    #                              'receiver_account': 'receiver_account', 'sender_country': 'sender_country',
    #                              'sender_municipality': 'sender_municipality', 'receiver_country': 'receiver_country',
    #                              'receiver_municipality': 'receiver_municipality',
    #                              'transaction_type': 'transaction_type', 'notes': 'notes'}

    df = pd.read_csv('data/sebank_customers_with_accounts.csv')
    df['municipality'] = df['Address'].str.split(' ').str[-1].str.strip()
    dict1 = df.to_dict('records')

    customers = []

    for round, row in enumerate(dict1):
        ssn = row['Personnummer']
        name = row['Customer']
        address = row['Address']
        phone = row['Phone']
        account_number = row['BankAccount']
        municipality = row['municipality']

        index = -1
        for i, customer in enumerate(customers):
            if customer["ssn"] == ssn:
                index = i
                break

        if index == -1:
            new_customer = {
                "name": name,
                "ssn": ssn,
                "address": address,
                "phone": phone,
                "municipality": municipality,
                "account_list": []
            }

            new_customer["account_list"].append(account_number)
            customers.append(new_customer)
        else:
            customers[index]["account_list"].append(account_number)

    try:
        with db.begin():
            for i, row in enumerate(customers):
                new_customer = Customer(name=row['name'], ssn=row['ssn'], address=row['address'], phone=row['phone'])
                db.add(new_customer)
                db.flush()
                for account in customers[i]['account_list']:
                    new_account = Account(
                                    account_number=account,
                                    municipality=customers[i]['municipality'],
                                    customer_id=new_customer.id)
                    db.add(new_account)
                    db.flush()
            db.commit()
            print('Import Account Successful!')
    except SQLAlchemyError as e:
        print("Unsuccesful Account import", e)
        db.rollback()
    db.close()


if __name__ == '__main__':
    customer_account_main()
