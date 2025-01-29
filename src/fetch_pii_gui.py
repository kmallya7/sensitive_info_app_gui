import os
import snowflake.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk

def fetch_pii_data():
    user = 'kmallya7'
    password = 'Udumalpet@7'
    account = 'hfgwbta-cf08090'
    warehouse = 'COMPUTE_WH'
    database = 'ABCINC'
    schema = 'ABCINC.PUBLIC'
    role = 'ACCOUNTADMIN'

    con = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role
    )

    query = """
    SELECT Name, Email, Phone, Address, Aadhar, PAN, Passport, License, CreditCardNumber, BankAccountNumber, TaxID
    FROM ENTERPRISEMASTERDATASET
    """

    df = pd.read_sql(query, con)
    con.close()

    # Explicitly replace NaN with "NONE"
    df = df.fillna("NONE")

    return df

def main():
    df = fetch_pii_data()

    # Save PII data to CSV
    df.to_csv('enterprise_pii_data.csv', index=False)
    print("CSV file has been generated: enterprise_pii_data.csv")

    # Create GUI window
    root = tk.Tk()
    root.title("Enterprise PII Data")

    # Create Treeview widget to display DataFrame
    tree = ttk.Treeview(root)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for row in df.itertuples(index=False, name=None):
        values = [value if value != "NONE" else "NONE" for value in row]
        tree.insert("", "end", values=values)

    tree.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

if __name__ == "__main__":
    main()
