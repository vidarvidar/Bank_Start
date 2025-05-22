#app.py för sqlalchemy + ETL
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine
from etlfuncs import csv_reader_renamer, db_table_trasher, db_adder


def main():

    db_table_trasher(Transaction)
    db_table_trasher(Account)

    # df = csv_reader_renamer('Accounts', 'data/sebank_customers_with_accounts.csv')
    # db_adder('Accounts', df)
    # df = csv_reader_renamer('Transactions', 'data/transactions.csv')
    # db_adder('Transactions', df)

if __name__ == '__main__':
    main()
