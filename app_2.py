from etlfuncs import *
from validate_transactions import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine



def main():
    db_table_trasher(Transaction)
    valid, invalid = validate_transactions('data/sample_transactions')



    df = valid.drop("approved", axis=1)
    transaction_column_mapper = {'transaction_id': 'id', 'timestamp': 'timestamp', 'amount': 'amount',
                                 'currency': 'currency', 'sender_account': 'sender_account',
                                 'receiver_account': 'receiver_account', 'sender_country': 'sender_country',
                                 'sender_municipality': 'sender_municipality', 'receiver_country': 'receiver_country',
                                 'receiver_municipality': 'receiver_municipality',
                                 'transaction_type': 'transaction_type', 'notes': 'notes'}
    df = df.rename(columns=transaction_column_mapper)
    db_adder("Transactions",df)
    # print(df)

if __name__ == '__main__':
    main()