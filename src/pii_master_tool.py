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

# Obfuscate PII data
def obfuscate_pii(df):
    pii_columns = ['AADHAR', 'PAN', 'CREDITCARDNUMBER', 'BANKACCOUNTNUMBER']
    obfuscated_df = df.copy()
    for column in pii_columns:
        if column in obfuscated_df.columns:
            obfuscated_df[column] = obfuscated_df[column].apply(lambda x: str(x)[:4] + '****' + str(x)[-4:] if pd.notnull(x) else '')
    return obfuscated_df

# Generate a CSV report
def generate_report(df):
    report_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if report_file:
        df.to_csv(report_file, index=False)
        print(f"Report saved to {report_file}")

# Display summary report as a table in the GUI
def display_summary_report(df, root):
    pii_columns = ['AADHAR', 'PAN', 'CREDITCARDNUMBER', 'BANKACCOUNTNUMBER']
    
    # Gather table and column names
    table_columns = [(table_name, column) for table_name in ['ENTERPRISEMASTERDATASET'] for column in pii_columns]
    
    # Count number of records affected
    record_counts = {column: df[column].count() for column in pii_columns}
    
    # Examples of detected sensitive data (obfuscated)
    examples = {column: df[column].apply(lambda x: str(x)[:4] + '****' + str(x)[-4:] if pd.notnull(x) else '') for column in pii_columns}
    
    # Create a summary DataFrame
    summary_data = {
        'Table Name': ['ENTERPRISEMASTERDATASET']*len(pii_columns),
        'Column Name': pii_columns,
        'Number of Records Affected': [record_counts[col] for col in pii_columns],
        'Example': [examples[col].iloc[0] for col in pii_columns]
    }
    summary_df = pd.DataFrame(summary_data)

    # Display summary as table
    summary_frame = tk.Frame(root)
    summary_frame.pack(pady=10)

    summary_columns = list(summary_df.columns)
    tree = ttk.Treeview(summary_frame, columns=summary_columns, show='headings')

    for col in summary_columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for index, row in summary_df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack()

    # Add export options
    export_txt_button = tk.Button(root, text="Export as TXT", command=lambda: export_summary_report_txt(summary_df))
    export_txt_button.pack(pady=5)

    export_img_button = tk.Button(root, text="Export as Image", command=lambda: export_summary_report_image(summary_frame))
    export_img_button.pack(pady=5)

def export_summary_report_txt(summary_df):
    summary_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if summary_file:
        with open(summary_file, 'w') as f:
            f.write(summary_df.to_string(index=False))
        print(f"Summary report saved to {summary_file}")

def export_summary_report_image(frame):
    import PIL.ImageGrab as ImageGrab
    
    x = frame.winfo_rootx()
    y = frame.winfo_rooty()
    width = x + frame.winfo_width()
    height = y + frame.winfo_height()

    image = ImageGrab.grab(bbox=(x, y, width, height))
    image_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if image_file:
        image.save(image_file)
        print(f"Summary report saved as image to {image_file}")

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

        summary_report_button = tk.Button(root, text="Generate Summary Report", command=lambda: display_summary_report(df, root))
        summary_report_button.pack(pady=10)

        obfuscate_csv_button = tk.Button(root, text="Obfuscate and Export CSV", command=lambda: obfuscate_and_export_csv(df))
        obfuscate_csv_button.pack(pady=10)
    else:
        print("Failed to fetch data.")

def obfuscate_and_export_csv(df):
    obfuscated_df = obfuscate_pii(df)
    report_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if report_file:
        obfuscated_df.to_csv(report_file, index=False)
        print(f"Obfuscated data saved to {report_file}")

if __name__ == "__main__":
    create_gui()
