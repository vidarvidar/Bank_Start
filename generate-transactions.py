import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

# Locale-specific faker instances
locale_map = {
    'Sweden': Faker('sv_SE'),
    'Norway': Faker('no_NO'),
    'Denmark': Faker('da_DK'),
    'Finland': Faker('fi_FI'),
    'Germany': Faker('de_DE'),
    'Poland': Faker('pl_PL'),
    'Estonia': Faker('et_EE'),
    'Island': Faker('is_IS'),
    'Iran': Faker('fa_IR'),
    'Myanmar': Faker('en_GB'),
    'North Korea': Faker('ko_KR'),
    'Swaziland': Faker('en_GB'),
    'France': Faker('fr_FR'),
    'United Kingdom': Faker('en_GB'),
    'United States of America': Faker('en_US'),
    'Japan': Faker('ja_JP'),
    'China': Faker('zh_CN'),
    'Russia': Faker('ru_RU'),
    'South Africa': Faker('en_GB'),
    'Zambia': Faker('en_GB'),
    'default': Faker('en_US')
}

# Configuration
NUM_TRANSACTIONS = 100000
KNOWN_ACCOUNTS_COUNT = 1000
SWEDISH_BANK_PREFIX = "SE8902"
BLACKLISTED_COUNTRIES = {'North Korea', 'Iran', 'Myanmar', 'Swaziland'}
BLACKLISTED_MUNICIPALITIES = {'Lesoto', 'Lagos', 'Caracas'}
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

# Country groups
NEIGHBOUR_COUNTRIES = {'Norway', 'Denmark', 'Finland', 'Germany', 'Estonia', 'Island', 'Poland'}
SWEDEN = 'Sweden'
TODAY = datetime(2025, 5, 19)

# Currency mapping
COUNTRY_CURRENCIES = {
    'Sweden': 'SEK',
    'Norway': 'NOK',
    'Denmark': 'DKK',
    'Finland': 'EUR',
    'Germany': 'EUR',
    'France': 'EUR',
    'United Kingdom': 'GBP',
    'United States of America': 'USD',
    'Japan': 'JPY',
    'Myanmar': 'RMB',
    'China': 'RMB',
    'Russia': 'RUB',
    'South Africa': 'ZAR',
    'Zambia': 'ZMW'
}

# Single default faker for fallbacks
default_fake = locale_map['default']

# Generate known accounts
known_accounts = {SWEDISH_BANK_PREFIX + default_fake.bban() for _ in range(KNOWN_ACCOUNTS_COUNT)}

# Helper functions
def swedish_account():
    return SWEDISH_BANK_PREFIX + default_fake.bban()

def random_foreign_account():
    return default_fake.iban()

def random_location(distribution="global"):
    if distribution == "sweden":
        return SWEDEN, locale_map.get('Sweden', default_fake).city()
    elif distribution == "neighbour":
        country = random.choice(list(NEIGHBOUR_COUNTRIES))
        city = locale_map.get(country, default_fake).city()
        return country, city
    else:
        country = default_fake.country()
        while country == SWEDEN or country in NEIGHBOUR_COUNTRIES:
            country = default_fake.country()
        city = locale_map.get(country, default_fake).city()
        return country, city

def resolve_currency(country):
    return COUNTRY_CURRENCIES.get(country, 'USD')

def is_suspicious(sender_country, receiver_country, sender_municipality, receiver_municipality, sender_account, receiver_account, amount):
    if sender_country in BLACKLISTED_COUNTRIES or receiver_country in BLACKLISTED_COUNTRIES:
        return True
    if sender_municipality in BLACKLISTED_MUNICIPALITIES or receiver_municipality in BLACKLISTED_MUNICIPALITIES:
        return True
    if (sender_account not in known_accounts or receiver_account not in known_accounts) and amount > 10000:
        return True
    return False

def create_transaction(timestamp, sender_account, receiver_account, sender_country, receiver_country, sender_municipality, receiver_municipality, amount, currency):
    transaction_id = str(uuid.uuid4())
    transaction_type = random.choice(['incoming', 'outgoing'])
    realistic_reasons = [
        'Salary payment', 'Utility bill', 'Online purchase', 'Rent transfer',
        'Loan repayment', 'Subscription fee', 'Mobile recharge',
        'Tax refund', 'Consulting fee', 'Insurance payout',
        'Reimbursement for travel', 'Payment for invoice #{}'.format(random.randint(1000, 9999)),
        'Gift to family member', 'Freelance project payment'
    ]
    notes = random.choice(realistic_reasons) if random.random() < 0.9 else None

    return [
        transaction_id, timestamp, round(amount, 2), currency, sender_account, receiver_account,
        sender_country, sender_municipality, receiver_country, receiver_municipality,
        transaction_type, notes
    ]

def distribution_decision():
    roll = random.random()
    if roll < 0.55:
        return "sweden"
    elif roll < 0.7:
        return "neighbour"
    else:
        return "global"

def generate_transactions(n):
    data = []
    start_date = TODAY.replace(month=1, day=1)

    within_bank_count = int(0.10 * n)
    normal_count = n - within_bank_count - BURST_ACCOUNT_COUNT * BURST_PER_ACCOUNT - SMURFING_ACCOUNT_COUNT * SMURFING_TARGETS_PER_ACCOUNT

    for _ in range(within_bank_count):
        timestamp = start_date + timedelta(days=random.randint(0, 137), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        sender = random.choice(list(known_accounts))
        receiver = random.choice(list(known_accounts))
        sender_country, sender_city = random_location("sweden")
        receiver_country, receiver_city = random_location("sweden")
        data.append(create_transaction(timestamp, sender, receiver, sender_country, receiver_country, sender_city, receiver_city, random.uniform(10, 50000), 'SEK'))

    for _ in range(normal_count):
        is_incoming = random.random() < 0.5
        dist = distribution_decision()
        timestamp = start_date + timedelta(days=random.randint(0, 137), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        if is_incoming:
            sender = random_foreign_account()
            receiver = random.choice(list(known_accounts))
            sender_country, sender_city = random_location(dist)
            receiver_country, receiver_city = random_location("sweden")
            currency = resolve_currency(sender_country)
        else:
            sender = random.choice(list(known_accounts))
            receiver = random_foreign_account()
            sender_country, sender_city = random_location("sweden")
            receiver_country, receiver_city = random_location(dist)
            currency = 'SEK'
        data.append(create_transaction(timestamp, sender, receiver, sender_country, receiver_country, sender_city, receiver_city, random.uniform(10, 50000), currency))

    for _ in range(BURST_ACCOUNT_COUNT):
        sender = random.choice(list(known_accounts))
        base_time = start_date + timedelta(days=random.randint(0, 137), hours=random.randint(9, 17))
        for _ in range(BURST_PER_ACCOUNT):
            receiver = random_foreign_account()
            ts = base_time + timedelta(seconds=random.randint(0, 300))
            s_city, r_city = random_location("sweden")[1], random_location("germany")[1]
            data.append(create_transaction(ts, sender, receiver, SWEDEN, "Germany", s_city, r_city, random.uniform(100, 1000), 'SEK'))

    for _ in range(SMURFING_ACCOUNT_COUNT):
        receiver = random.choice(list(known_accounts))
        for _ in range(SMURFING_TARGETS_PER_ACCOUNT):
            sender = random_foreign_account()
            ts = start_date + timedelta(days=random.randint(0, 137), hours=random.randint(8, 18))
            s_country, s_city = random_location("global")
            r_country, r_city = SWEDEN, random_location("sweden")[1]
            currency = resolve_currency(s_country)
            data.append(create_transaction(ts, sender, receiver, s_country, r_country, s_city, r_city, random.uniform(5, 200), currency))

    df = pd.DataFrame(data, columns=[
        'transaction_id', 'timestamp', 'amount', 'currency', 'sender_account', 'receiver_account',
        'sender_country', 'sender_municipality', 'receiver_country', 'receiver_municipality',
        'transaction_type', 'notes'
    ])

    for col in ['sender_country', 'receiver_country', 'sender_municipality', 'receiver_municipality']:
        df.loc[df.sample(frac=MISSING_VALUE_PERCENTAGE).index, col] = None

    anomaly_count = int(BACKDATE_FORWARD_DATE_PERCENTAGE * len(df))
    sampled_back = df.sample(anomaly_count).copy()
    df.loc[sampled_back.index, 'timestamp'] = sampled_back['timestamp'] - pd.to_timedelta(
        np.random.randint(365, 1000, size=anomaly_count), unit='d')

    sampled_forward = df.sample(anomaly_count).copy()
    df.loc[sampled_forward.index, 'timestamp'] = sampled_forward['timestamp'] + pd.to_timedelta(
        np.random.randint(1, 365, size=anomaly_count), unit='d')

    return df

if __name__ == "__main__":
    print("Generating synthetic transactions for Swedish bank scenario with fraud patterns...")
    df = generate_transactions(NUM_TRANSACTIONS)
    df.to_csv("data/transactions.csv", index=False)
    print("Saved to data/transactions.csv")
