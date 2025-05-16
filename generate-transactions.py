import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

fake = Faker()

# Configuration
NUM_TRANSACTIONS = 10000
KNOWN_ACCOUNTS_COUNT = 1000
BLACKLISTED_COUNTRIES = {'North Korea', 'Iran', 'Syria'}
BLACKLISTED_MUNICIPALITIES = {'Fraudtown', 'Scamville'}
DUPLICATE_PERCENTAGE = 0.01
NEAR_DUPLICATE_PERCENTAGE = 0.01
MISSING_VALUE_PERCENTAGE = 0.005
NOISE_NOTES_PERCENTAGE = 0.1
NIGHT_TRANSACTION_PERCENTAGE = 0.03
BURST_ACCOUNT_COUNT = 50
BURST_PER_ACCOUNT = 100
SMURFING_ACCOUNT_COUNT = 30
SMURFING_TARGETS_PER_ACCOUNT = 10
BACKDATE_FORWARD_DATE_PERCENTAGE = 0.01

# Generate known accounts
known_accounts = {fake.iban() for _ in range(KNOWN_ACCOUNTS_COUNT)}

# Helper functions
def random_account():
    return fake.iban()

def random_location():
    country = fake.country()
    municipality = fake.city()
    return country, municipality

def is_suspicious(sender_country, receiver_country, sender_municipality, receiver_municipality, sender_account, receiver_account, amount):
    if sender_country in BLACKLISTED_COUNTRIES or receiver_country in BLACKLISTED_COUNTRIES:
        return True
    if sender_municipality in BLACKLISTED_MUNICIPALITIES or receiver_municipality in BLACKLISTED_MUNICIPALITIES:
        return True
    if (sender_account not in known_accounts or receiver_account not in known_accounts) and amount > 10000:
        return True
    return False

# Generate a single transaction
def create_transaction(timestamp, sender_account, receiver_account, amount=None):
    transaction_id = str(uuid.uuid4())
    amount = round(amount if amount else random.uniform(10, 50000), 2)
    currency = random.choice(['USD', 'EUR', 'GBP', 'SEK'])

    sender_country, sender_municipality = random_location()
    receiver_country, receiver_municipality = random_location()
    transaction_type = random.choice(['transfer', 'deposit', 'withdrawal', 'payment'])
    flagged = is_suspicious(sender_country, receiver_country, sender_municipality, receiver_municipality, sender_account, receiver_account, amount)
    is_known = sender_account in known_accounts or receiver_account in known_accounts

    notes = None
    if random.random() < NOISE_NOTES_PERCENTAGE:
        notes = fake.sentence(nb_words=random.randint(3, 12))

    return [
        transaction_id, timestamp, amount, currency, sender_account, receiver_account,
        sender_country, sender_municipality, receiver_country, receiver_municipality,
        is_known, flagged, transaction_type, notes
    ]

# Generate transactions
def generate_transactions(n):
    data = []
    start_date = datetime(2023, 1, 1)

    # Regular transactions
    for i in range(n):
        if random.random() < NIGHT_TRANSACTION_PERCENTAGE:
            hour = random.randint(0, 5)
        else:
            hour = random.randint(6, 23)
        timestamp = start_date + timedelta(days=random.randint(0, 364), hours=hour, minutes=random.randint(0, 59), seconds=random.randint(0, 59))

        sender_account = random.choice(list(known_accounts)) if random.random() < 0.7 else random_account()
        receiver_account = random.choice(list(known_accounts)) if random.random() < 0.7 else random_account()

        transaction = create_transaction(timestamp, sender_account, receiver_account)
        data.append(transaction)

    # Bursts from same sender
    burst_senders = random.sample(list(known_accounts), BURST_ACCOUNT_COUNT)
    for sender in burst_senders:
        burst_time = start_date + timedelta(days=random.randint(0, 364), hours=random.randint(9, 17))
        for _ in range(BURST_PER_ACCOUNT):
            receiver = random_account()
            ts = burst_time + timedelta(seconds=random.randint(0, 300))
            data.append(create_transaction(ts, sender, receiver))

    # Smurfing: many small transactions to same receiver
    for _ in range(SMURFING_ACCOUNT_COUNT):
        receiver = random.choice(list(known_accounts))
        for _ in range(SMURFING_TARGETS_PER_ACCOUNT):
            sender = random_account()
            ts = start_date + timedelta(days=random.randint(0, 364), hours=random.randint(8, 18))
            data.append(create_transaction(ts, sender, receiver, amount=random.uniform(5, 200)))

    # Add exact duplicates
    df = pd.DataFrame(data, columns=[
        'transaction_id', 'timestamp', 'amount', 'currency', 'sender_account', 'receiver_account',
        'sender_country', 'sender_municipality', 'receiver_country', 'receiver_municipality',
        'is_in_customer_db', 'is_flagged', 'transaction_type', 'notes'
    ])
    num_duplicates = int(DUPLICATE_PERCENTAGE * n)
    duplicates = df.sample(n=num_duplicates, replace=True).copy()
    duplicates['transaction_id'] = [str(uuid.uuid4()) for _ in range(num_duplicates)]
    df = pd.concat([df, duplicates], ignore_index=True)

    # Add near duplicates
    num_near_duplicates = int(NEAR_DUPLICATE_PERCENTAGE * n)
    near_duplicates = df.sample(n=num_near_duplicates, replace=True).copy()
    for i in range(num_near_duplicates):
        near_duplicates.iloc[i]['amount'] *= random.uniform(0.98, 1.02)
        near_duplicates.iloc[i]['timestamp'] += timedelta(seconds=random.randint(-60, 60))
        near_duplicates.iloc[i]['transaction_id'] = str(uuid.uuid4())
    df = pd.concat([df, near_duplicates], ignore_index=True)

    # Introduce missing values
    for col in ['sender_country', 'receiver_country', 'sender_municipality', 'receiver_municipality']:
        df.loc[df.sample(frac=MISSING_VALUE_PERCENTAGE).index, col] = None

    # Timestamp anomalies
    anomaly_count = int(BACKDATE_FORWARD_DATE_PERCENTAGE * n)
    backdate_rows = df.sample(n=anomaly_count).copy()
    future_rows = df.sample(n=anomaly_count).copy()
    df.loc[backdate_rows.index, 'timestamp'] = df.loc[backdate_rows.index, 'timestamp'] - pd.to_timedelta(np.random.randint(365, 1000, size=anomaly_count), unit='d')
    df.loc[future_rows.index, 'timestamp'] = df.loc[future_rows.index, 'timestamp'] + pd.to_timedelta(np.random.randint(1, 365, size=anomaly_count), unit='d')

    return df

# Main execution
if __name__ == "__main__":
    print("Generating enhanced synthetic financial transactions dataset...")
    df = generate_transactions(NUM_TRANSACTIONS)
    df.to_csv("data/transactions.csv", index=False)
    print("Saved to data/transactions.csv")
