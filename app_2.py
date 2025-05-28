
from validate_transactions import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Account, Transaction
from db_sqlalchemy import init_db, engine



def import_transactions():
# main funktion som kör transactions från csv fil - igenom validering - och i slutet till databas
    init_db()
    db = Session(engine)
    db.query(Transaction).delete()
    db.commit()
    valid, invalid = validate_transactions('data/transactions.csv')
    # från validate_transactions.py importerar vi validate_transactions funktionen som tar han om att läsa av csv'n til dataframe
    # data tvättas och filtreras och i slutet körs den igenom vår expectation suite med GX. Från det får vi 2 dataframes,
    # en med valid transactions och en med invalid.
    account_numbers = []
    for number in db.query(Account.account_number).all():
        account_numbers.append(number.account_number)
    # Skapa lista av account numbers som vi jämför med inkommande transactions

    valid = valid.drop("approved", axis=1)
    transaction_column_mapper = {'transaction_id': 'id', 'timestamp': 'timestamp', 'amount': 'amount',
                                 'currency': 'currency', 'sender_account': 'sender_account',
                                 'receiver_account': 'receiver_account', 'sender_country': 'sender_country',
                                 'sender_municipality': 'sender_municipality', 'receiver_country': 'receiver_country',
                                 'receiver_municipality': 'receiver_municipality',
                                 'transaction_type': 'transaction_type', 'notes': 'notes'}
    valid = valid.rename(columns=transaction_column_mapper)
    # För att kunna köra dataframen direkt til databasen så döper vi över alla kolumner så de matchar tabellen i dben.

    try:
        invalid_list = []    # Lista där vi lägger til de transactions som inte passerar genom nedanstående validering. Den kan eventuellt bli mergad med invalid dataframe'n ovanför
        for i, r in valid.iterrows():
            if r['transaction_type'] == 'outgoing':
                # current_account = db.query(Account).filter(Account.account_number == r['sender_account']).one_or_none()
                if not r['sender_account'] in account_numbers:
                    invalid_list.append(r)
                    valid.drop(i, axis=0, inplace=True)
                # elif not r['sender_municipality'] in current_account.municipality:
                #     invalid_list.append(r)
                #     print(
                #         f'Invalid transaction {r['transaction_id']}, sender municipality {r["sender_municipality"]} does not match account municipality {current_account.municipality}',
                #         len(valid))
                #     valid.drop(i, axis=0, inplace=True)
                else:
                    transaction = Transaction(**r)
                    db.add(transaction)

            elif r['transaction_type'] == 'incoming':
                # current_account = db.query(Account).filter(Account.account_number == r['receiver_account']).one_or_none()
                if not r['receiver_account'] in account_numbers:
                    invalid_list.append(r)
                    valid.drop(i, axis=0, inplace=True)
                # elif not r['receiver_municipality'] in current_account.municipality:
                #     invalid_list.append(r)
                #     print(
                #         f'Invalid transaction {r['transaction_id']}, receiver municipality {r["sender_municipality"]} does not match account municipality {current_account.municipality}',
                #         len(valid))
                #     valid.drop(i, axis=0, inplace=True)
                else:
                    transaction = Transaction(**r)
                    db.add(transaction)

        db.commit()
        print('Import Transactions Successful!')
        print(len(invalid_list), 'items in invalid list,', len(valid), 'items in valid list')
        db.close()
    except SQLAlchemyError as e:
        print("Unsuccesful Transaction import:", e)
        db.rollback()
        db.close()
    # Loopar igenom hela dataframen för att plocka ut transactions där sender_account eller receiver_account inte finns
    # i vår bank. Här använder vi transaction_type, outgoing eller incoming, som nyckel. Om en transaktion är outgoing då måste
    # den komma från konto som tillhör vår bank, och om den är incoming då måste receiver account tillhöra vår bank.

    # Här ovanför har vi också skrivit kod som skulle plocka ut om sender/receiver municipality inte matchar med den staden som
    # står på deras konto och kundregister. Men det visar sig att nästan alla transaktioner faller på den filteringen, av 100000
    # transaktioner står det ungefär 1200 kvar. Vi tror inte att de är meningen att de skulle vara så, därför lämnar vi den utkommenterat.
    # För att se test av den filtering, finns den i etl_app_notebook filen där vi har testat at köra dataframe igenom filteringen utan att överföra den til databasen.

if __name__ == '__main__':
    import_transactions()