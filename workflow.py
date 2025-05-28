from prefect import flow, task
from validate_transactions import validate_transactions
from sqlalchemy_app import customer_account_main

@task
def add_customers():
    customer_account_main()

@task
def run_validation():
    valid, invalid, results = validate_transactions("data/sample_transactions")
    return results

@flow
def main():
    add_customers()
    results = run_validation()
    print(results.result())

if __name__ == '__main__':
    main()