import pandas as pd
from db_logic import create_tables, insert_csv_to_db, save_mismatches_to_db
from email_logic import send_email_with_attachments

def compare_values(val1, val2):
    if pd.isna(val1) and pd.isna(val2):
        return True
    return val1 == val2

def read_csv_files(bank_file, internal_file):
    df_bank = pd.read_csv(bank_file)
    df_internal = pd.read_csv(internal_file)
    return df_bank, df_internal

def merge_and_match(df_bank, df_internal):
    merged_df = pd.merge(df_bank, df_internal, on='Reference Number', suffixes=('_bank', '_internal'))
    merged_df['Debit_Match'] = merged_df.apply(lambda row: compare_values(row['Debit_bank'], row['Debit_internal']), axis=1)
    merged_df['Credit_Match'] = merged_df.apply(lambda row: compare_values(row['Credit_bank'], row['Credit_internal']), axis=1)
    merged_df['Is_Matched'] = merged_df['Debit_Match'] & merged_df['Credit_Match']
    return merged_df

def generate_summary(merged_df):
    total = len(merged_df)
    matched = merged_df['Is_Matched'].sum()
    mismatched = total - matched
    return total, matched, mismatched

def export_results(mismatches_df, total, matched, mismatched):
    match_percentage = (matched / total) * 100
    mismatch_percentage = 100 - match_percentage

    mismatches_df.to_csv("mismatched_transactions.csv", index=False)

    with open("summary_report.txt", "w") as file:
        file.write("== Summary Report ==\n")
        file.write(f"Total Transactions: {total}\n")
        file.write(f"Matched Transactions: {matched} ({match_percentage:.2f}%)\n")
        file.write(f"Mismatched Transactions: {mismatched} ({mismatch_percentage:.2f}%)\n")

    print("✅ Export completed")

def main():
    create_tables()

    bank_file = 'bank_statement.csv'
    internal_file = 'internal_record.csv'

    insert_csv_to_db(bank_file, internal_file)

    df_bank, df_internal = read_csv_files(bank_file, internal_file)
    merged_df = merge_and_match(df_bank, df_internal)

    mismatches_df = merged_df[~merged_df['Is_Matched']]
    save_mismatches_to_db(mismatches_df)

    print("\n=== Mismatched Transactions ===")
    print(mismatches_df[['Reference Number', 'Debit_bank', 'Debit_internal', 'Credit_bank', 'Credit_internal']])

    total, matched, mismatched = generate_summary(merged_df)
    print("\n== Summary Report ==")
    print(f"Total Transactions: {total}")
    print(f"Matched Transactions: {matched}")
    print(f"Mismatched Transactions: {mismatched}")
    
    export_results(mismatches_df, total, matched, mismatched)
    send_email_with_attachments()

if __name__ == "__main__":
    main()
