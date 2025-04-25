import sqlite3
import pandas as pd

DB_NAME = "transactions.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_statement (
            reference_number TEXT PRIMARY KEY,
            debit REAL,
            credit REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internal_record (
            reference_number TEXT PRIMARY KEY,
            debit REAL,
            credit REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mismatched_transactions (
            reference_number TEXT PRIMARY KEY,
            debit_bank REAL,
            debit_internal REAL,
            credit_bank REAL,
            credit_internal REAL
        )
    """)

    conn.commit()
    conn.close()

def insert_csv_to_db(bank_csv, internal_csv):
    conn = sqlite3.connect(DB_NAME)

    # Load only the first 3 columns explicitly from both CSVs
    df_bank = pd.read_csv(bank_csv, usecols=[0, 1, 2])
    df_internal = pd.read_csv(internal_csv, usecols=[0, 1, 2])

    # Rename the columns to match the expected names
    df_bank.columns = ['reference_number', 'debit', 'credit']
    df_internal.columns = ['reference_number', 'debit', 'credit']

    # Insert data into the database tables
    df_bank.to_sql('bank_statement', conn, if_exists='replace', index=False)
    df_internal.to_sql('internal_record', conn, if_exists='replace', index=False)

    conn.close()
    print("✅ CSV data inserted into SQL database")
    
def save_mismatches_to_db(mismatches_df):
    conn = sqlite3.connect(DB_NAME)

    output_df = mismatches_df[['Reference Number', 'Debit_bank', 'Debit_internal', 'Credit_bank', 'Credit_internal']]
    output_df.columns = ['reference_number', 'debit_bank', 'debit_internal', 'credit_bank', 'credit_internal']

    output_df.to_sql('mismatched_transactions', conn, if_exists='replace', index=False)

    conn.close()
    print("✅ Mismatched data saved to the database.")
