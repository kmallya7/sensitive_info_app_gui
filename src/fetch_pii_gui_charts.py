import pandas as pd
import snowflake.connector
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt

# Fetch data from Snowflake
def fetch_data():
    try:
        # Set Snowflake credentials
        user = 'kmallya7'
        password = 'Udumalpet@7'
        account = 'hfgwbta-cf08090'
        warehouse = 'COMPUTE_WH'
        database = 'ABCINC'
        schema = 'ABCINC.PUBLIC'
        role = 'ACCOUNTADMIN'

        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema,
            role=role
        )

        query = "SELECT * FROM ENTERPRISEMASTERDATASET"
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("No data fetched from the query.")
            return None

        print("Data fetched successfully.")
        print("Column Names:", df.columns.tolist())  # Print column names for reference
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Generate a CSV report
def generate_report(df):
    report_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if report_file:
        df.to_csv(report_file, index=False)
        print(f"Report saved to {report_file}")

# Generate a pie chart for PII proportions
def generate_pie_chart(df):
    pii_columns = ['AADHAR', 'PAN', 'CREDITCARDNUMBER', 'BANKACCOUNTNUMBER']
    pii_counts = df[pii_columns].count()
    pii_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Proportion of PII Data')
    plt.ylabel('')  # Hide the y-axis label
    plt.show()

# Generate a horizontal bar chart for PII counts
def generate_horizontal_bar_chart(df):
    pii_columns = ['AADHAR', 'PAN', 'CREDITCARDNUMBER', 'BANKACCOUNTNUMBER']
    pii_counts = df[pii_columns].count()
    pii_counts.plot(kind='barh')
    plt.title('Count of PII Data')
    plt.xlabel('Count')
    plt.ylabel('PII Type')
    plt.show()

# Display data in a table format
def display_table(root, df):
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    columns = list(df.columns)
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack()

# Create the GUI
def create_gui():
    global root
    root = tk.Tk()
    root.title("Sensitive Info App GUI - Charts")

    fetch_button = tk.Button(root, text="Fetch Data", command=lambda: fetch_and_display_data())
    fetch_button.pack(pady=10)

    root.mainloop()

# Fetch data and display it in the GUI
def fetch_and_display_data():
    df = fetch_data()
    if df is not None:
        display_table(root, df)

        # Add buttons to generate report and charts
        report_button = tk.Button(root, text="Generate Report", command=lambda: generate_report(df))
        report_button.pack(pady=10)

        pie_chart_button = tk.Button(root, text="Generate Pie Chart", command=lambda: generate_pie_chart(df))
        pie_chart_button.pack(pady=10)

        horizontal_bar_chart_button = tk.Button(root, text="Generate Horizontal Bar Chart", command=lambda: generate_horizontal_bar_chart(df))
        horizontal_bar_chart_button.pack(pady=10)
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    create_gui()
