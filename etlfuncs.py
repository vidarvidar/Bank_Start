# funcions used in ETL process
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine

def db_table_trasher(Table):
    init_db()
    db = Session(bind=engine)
    db.query(Table).delete()
    db.commit()
    db.close()

def csv_reader_renamer(table, path):

    account_column_mapper = {'Customer': 'customer', 'Address': 'address', 'Phone': 'phone', 'Personnummer': 'ssn',
                             'BankAccount': 'account_number'}
    transaction_column_mapper = {'transaction_id': 'id', 'timestamp': 'timestamp', 'amount': 'amount',
                                 'currency': 'currency', 'sender_account': 'sender_account',
                                 'receiver_account': 'receiver_account', 'sender_country': 'sender_country',
                                 'sender_municipality': 'sender_municipality', 'receiver_country': 'receiver_country',
                                 'receiver_municipality': 'receiver_municipality',
                                 'transaction_type': 'transaction_type', 'notes': 'notes'}
    if table == 'Transactions':
        df = pd.read_csv(path)
        df = df.rename(columns=transaction_column_mapper)
        return df
    if table == 'Accounts':
        df = pd.read_csv(path)
        df = df.rename(columns=account_column_mapper)
        return df
    else:
        print('Table must be either Transactions or Accounts')

def db_adder(table, df):
    init_db()
    db = Session(engine)
    if table == 'Transactions':
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
    if table == 'Accounts':
        try:
            with db.begin():
                for row in df.to_dict('records'):
                    account = Account(**row)
                    db.add(account)
                    db.flush()
                db.commit()
                print('Import Account Successful!')
        except SQLAlchemyError as e:
            print("Unsuccesful Account import", e)
            db.rollback()
    db.close()
