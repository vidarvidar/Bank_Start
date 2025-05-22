# för att testa om sqlalchemy funkar med databasen
from locale import currency

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine
#
def main():
    init_db()
    db = Session(engine)
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.commit()
    account_column_mapper = {'Customer': 'customer', 'Address': 'address', 'Phone': 'phone', 'Personnummer': 'ssn', 'BankAccount':'account_number'}
    transaction_column_mapper = {'transaction_id': 'id','timestamp':'timestamp','amount':'amount','currency':'currency','sender_account':'sender_account','receiver_account':'receiver_account','sender_country':'sender_country','sender_municipality':'sender_municipality','receiver_country':'receiver_country','receiver_municipality':'receiver_municipality','transaction_type':'transaction_type','notes':'notes'}

    df = pd.read_csv('data/sebank_customers_with_accounts.csv')
    df = df.rename(columns=account_column_mapper)

    # dict1 = df[['name', 'address', 'ssn', 'phone']].drop_duplicates().to_dict('records')
    # dict2 = df[['account_number', 'ssn']].to_dict('records')

    try:
        with db.begin():

            for row1 in df.to_dict('records'):
                account = Account(account_number=row1['account_number'], customer=row1['customer'], ssn=row1['ssn'], address=row1['address'], phone=row1['phone'])
                db.add(account)
                db.flush()

            db.commit()
            print('Import Accounts Successful!')

    except SQLAlchemyError as e:
        print("Unsuccesful Account import", e)
        db.rollback()

    df = pd.read_csv('data/transactions.csv')
    df = df.rename(columns=transaction_column_mapper)

    try:
        with db.begin():
            for row in df.to_dict('records'):
                transaction = Transaction(**row)
                db.add(transaction)
                db.flush()
            db.commit()
            print('Import Transactions Successful!')
    except SQLAlchemyError as e:
        print("Unsuccesful Transaction import", e)
        db.rollback()

    # timestamp=row['timestamp'], amount=row['amount'], currency=row['currency'],sender_account=row['sender_account'], receiver_account=row['receiver_account'], sender_country=row['sender_country']
    db.close()

if __name__ == '__main__':
    main()
