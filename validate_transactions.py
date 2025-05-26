def validate_transactions(filepath: str):
    import great_expectations as gx
    import pandas as pd
    import warnings
    import datetime as datetime
    warnings.filterwarnings("ignore", message="`result_format` configured at the Validator-level*")

    # Load the data
    df = pd.read_csv(filepath)

    # Regex for amount(Any number + "." + Any number): ^\d+\.\d+$
    amount_pattern = r"^-?\d+\.\d+$"
    # Regex for currency(Three uppercase letters): ^[A-Z]{3}$
    currency_pattern = r"^[A-Z]{3}$"
    # Regex for timestamp format: ^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$
    timestamp_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"

    # Fixes wrong spacing in amount
    def keep_only_last_dot(s):
        if pd.isna(s):
            return s
        s = str(s).replace(" ", "").replace(".", "")  # Remove spaces and existing dots
        if len(s) > 2:
            return s[:-2] + "." + s[-2:]
        return s

    # Apply to DataFrame
    df["amount"] = df["amount"].apply(keep_only_last_dot)

    # Fixes amount
    df["amount"] = pd.to_numeric(df["amount"])  # Convert to numeric
    df["amount"] = df["amount"].astype(float)  # Convert to float

    # Fixes currency (removes spaces)
    df["currency"] = df["currency"].astype(str).str.replace(" ", "")

    formats_to_try_currency = [
        "SEK",
        "DKK",
        "USD",
        "EUR",
        "NOK",
        "RMB",
        "ZAR",
        "GBP",
        "ZMW",
        "JPY"
    ]

    # Fixes datetime format
    formats_to_try_datetime = [
        "%Y%m%d %H:%M:%S",
        "%y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H.%M",
        "%Y-%m-%d %H.%M:%S",
        "%Y-%m-%d %H.%M.%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y.%m.%d %H.%M.%S"
    ]

    def parse_and_format(date_str):
        for fmt in formats_to_try_datetime:
            try:
                return datetime.datetime.strptime(date_str, fmt).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        return None

    df["timestamp"] = df["timestamp"].apply(parse_and_format)

    filtered_df = df[
        (df["transaction_type"] == "outgoing") &
        (df["sender_account"].str[:2] != "SE")
        ]

    # Create the ephemeral GX context
    context = gx.get_context()

    # Add a pandas datasource
    data_source = context.data_sources.add_pandas(name="pandas")

    # Add a dataframe asset
    data_asset = data_source.add_dataframe_asset(name="transactions_data")

    # Define the batch (entire DataFrame)
    batch_definition = data_asset.add_batch_definition_whole_dataframe(name="batch_def")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    # Create the expectation suite with a name
    suite = gx.core.expectation_suite.ExpectationSuite(name="transactions_suite")

    # Get the validator using the suite
    validator = context.get_validator(batch=batch, expectation_suite=suite)

    # Add expectations
    validator.expect_column_values_to_be_between("amount", min_value=0.01, max_value=100000)
    validator.expect_column_values_to_match_regex("amount", regex=amount_pattern)

    validator.expect_column_values_to_match_regex("currency", regex=currency_pattern)
    validator.expect_column_values_to_be_in_set("currency", value_set=formats_to_try_currency)

    validator.expect_column_values_to_match_regex("timestamp", regex=timestamp_pattern)

    validator.expect_column_values_to_not_be_null("transaction_id")
    # validator.expect_column_values_to_not_be_null("timestamp")
    # validator.expect_column_values_to_not_be_null("amount")
    # validator.expect_column_values_to_not_be_null("currency")
    validator.expect_column_values_to_not_be_null("sender_account")
    validator.expect_column_values_to_not_be_null("receiver_account")
    validator.expect_column_values_to_not_be_null("sender_country")
    validator.expect_column_values_to_not_be_null("sender_municipality")
    validator.expect_column_values_to_not_be_null("receiver_country")
    validator.expect_column_values_to_not_be_null("sender_municipality")
    validator.expect_column_values_to_not_be_null("transaction_type")

    # Validate
    results = validator.validate(result_format="COMPLETE")

    # Print results
    print(results)

    # Checks results for any unexpected counts.
    # Put Unexpected into an invalid DF and expected into a valid DF

    unexpected_transactions = [
        invalid_index
        for result in results["results"]
        for invalid_index in result["result"].get("unexpected_index_list", [])
    ]

    invalid_transactions = df.iloc[unexpected_transactions].copy()  # List to iloc
    valid_transactions = df.drop(index=unexpected_transactions)  # Drop invalid rows from valid df
    valid_transactions = df.drop(index=filtered_df.index)  # Drop the filtered rows form valid df

    invalid_transactions["approved"] = False
    valid_transactions["approved"] = True

    print(f"There are: {len(df)} Transaction entries.")
    print(f"Invalid Transactions: {len(invalid_transactions) + len(filtered_df)}")
    print(f"Valid Transactions: {len(valid_transactions)}")

    print(f"Dropped {len(invalid_transactions)} invalid_transactions from valid_transactions.")
    print(f"Dropped {len(filtered_df)} filtered transactions from valid_transactions")

    return valid_transactions, invalid_transactions