# för att testa om sqlalchemy funkar med databasen

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine

def main():
    init_db()
    db = Session(engine)
    db.query(Account).delete()
    db.query(Transaction).delete()
    db.commit()
    column_mapper = {'Customer': 'customer', 'Address': 'address', 'Phone': 'phone', 'Personnummer': 'ssn', 'BankAccount':'account_number'}

    df = pd.read_csv('data/sebank_customers_with_accounts.csv')
    df = df.rename(columns=column_mapper)

    # dict1 = df[['name', 'address', 'ssn', 'phone']].drop_duplicates().to_dict('records')
    # dict2 = df[['account_number', 'ssn']].to_dict('records')

    try:
        with db.begin():

            for row1 in df.to_dict('records'):
                account = Account(account_number=row1['account_number'], customer=row1['customer'], ssn=row1['ssn'], address=row1['address'], phone=row1['phone'])
                db.add(account)
                db.flush()

            # for row2 in dict2:
            #     account = Account(account_number=row2['account_number'], account_holder=row2['ssn'])
            #     db.add(account)
            #     db.flush()

            db.commit()
            print('Import Successful!')

    except SQLAlchemyError as e:
        print("Unsuccesful import", e)
        db.rollback()

    # try:
    #     with db.begin():
    #         for row in df[['account_number']].to_dict('records'):
    #             account = Account(account_number=row['account_number'], account_holder=customer.id)
    #             db.add(account)
    #         db.commit()
    #         print('Import Account Successful!')
    # except SQLAlchemyError as e:
    #     print("Unsuccesful import", e)
    #     db.rollback()


    db.close()

if __name__ == '__main__':
    main()
