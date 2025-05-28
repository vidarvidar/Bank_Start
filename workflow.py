from prefect import flow, task
from sqlalchemy_app import customer_account_main
from app_2 import import_transactions

@task
def add_customers():
    print("Running customer_account_main...")
    customer_account_main()

@task
def import_validated_transactions():
    print("Validating and importing transactions...")
    import_transactions()

@flow
def workflow():
    add_customers()
    import_validated_transactions()

if __name__ == '__main__':
    workflow()