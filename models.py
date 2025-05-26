from sqlalchemy import Column, String, Numeric, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):

    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    ssn = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)

    accounts = relationship('Account', back_populates='customer')

    def __init__(self, name, ssn, address, phone):
        self.name = name
        self.address = address
        self.ssn = ssn
        self.phone = phone
        self.account_list = []

    def __repr__(self):
        return f'{self.name} with SSN: {self.ssn} has address: {self.address} and phonenumber: {self.phone}'

    def add_account(self, account_number, municipality, customer_id):
        self.account_list.append(account_number)
        new_account = Account(account_number=account_number, municipality=municipality, customer_id=customer_id)
        return new_account


class Account(Base):

    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    account_number = Column(String, unique=True, nullable=False)
    municipality = Column(String, nullable=False)
    balance = Column(Numeric, default=0, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    # customer = Column(String, nullable=False)
    # address = Column(String, nullable=False)
    # ssn = Column(String, nullable=False)
    # phone = Column(String, nullable=True)



    customer = relationship('Customer', back_populates='accounts')

    def __init__(self, account_number, municipality, customer_id):
        self.account_number = account_number
        self.municipality = municipality
        self.customer_id = customer_id

        # self.customer = customer
        # self.address = address
        # self.ssn = ssn
        # self.phone = phone

    def __repr__(self):
        return f'{self.account_number} has balance of {self.balance}'

class Transaction(Base):

    __tablename__ = 'transactions'
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    sender_account = Column(String, nullable=False)
    receiver_account = Column(String, nullable=False)
    sender_country = Column(String, nullable=False)
    sender_municipality = Column(String, nullable=False)
    receiver_country= Column(String, nullable=False)
    receiver_municipality = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __init__(self, id, timestamp, amount, currency, sender_account, receiver_account, sender_country, sender_municipality, receiver_country, receiver_municipality, transaction_type, notes):
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.currency = currency
        self.sender_account = sender_account
        self.receiver_account = receiver_account
        self.sender_country = sender_country
        self.sender_municipality = sender_municipality
        self.receiver_country = receiver_country
        self.receiver_municipality = receiver_municipality
        self.transaction_type = transaction_type
        self.notes = notes

    def __repr__(self):
        return f'Transaction {self.id} of {self.amount} {self.currency} from {self.sender_account} to {self.receiver_account} occurred at {self.timestamp}'


