from tkinter import *
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import pandas as pd
from datetime import datetime

root = Tk()
root.title("Krittracker")

def add_expense():
    global df
    date = date_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()

    if date and amount and category:
        try:
            # Append new expense to CSV file
            with open("Record.csv", "a") as f:
                f.write(f"{date},{amount},{category}\n")  # Write new entry

            # Clear input fields
            date_entry.delete(0, END)
            amount_entry.delete(0, END)
            category_entry.delete(0, END)

            # Update DataFrame and tree view
            df = load_and_clean_data()
            update_treeview(df)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def load_and_clean_data():
    try:
        df = pd.read_csv("Record.csv", names=['Date', 'Amount', 'Category'])
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df.dropna(inplace=True)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Amount', 'Category'])

def update_treeview(df):
    # Clear existing items in treeview
    for item in tree.get_children():
        tree.delete(item)

    # Read from CSV and populate treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['Date'], row['Amount'], row['Category']))

def visualize_expenses_bar_chart():
    dates = []
    amounts = []
    with open("Record.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dates.append(row[0])
            amounts.append(float(row[1]))

    plt.bar(dates, amounts)
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Expense Bar Chart')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

def visualize_expenses_pie_chart():
    categories = {}
    with open("Record.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            category = row[2]
            amount = float(row[1])
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

    labels = list(categories.keys())
    sizes = list(categories.values())

    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Expense Pie Chart')
    plt.show()

def visualize_expenses_line_chart():
    dates = []
    amounts = []
    with open("Record.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dates.append(datetime.strptime(row[0], "%Y-%m-%d"))
            amounts.append(float(row[1]))

    plt.plot(dates, amounts)
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Expense Line Chart')
    plt.show()

def read_from_multiple_files(file_paths):
    dfs = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def write_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

def write_to_json(df, file_path):
    df.to_json(file_path, orient='records', indent=4)

# Load initial data
df = load_and_clean_data()

# Input fields for expense entry
Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = Entry(root)
date_entry.grid(row=0, column=1)

Label(root, text="Amount").grid(row=1, column=0)
amount_entry = Entry(root)
amount_entry.grid(row=1, column=1)

Label(root, text="Category").grid(row=2, column=0)
category_entry = Entry(root)
category_entry.grid(row=2, column=1)

Button(root, text="Add Expense", command=add_expense).grid(row=3, columnspan=2)

# Buttons to visualize expenses
Button(root, text="Bar Chart", command=visualize_expenses_bar_chart).grid(row=4, column=0)
Button(root, text="Pie Chart", command=visualize_expenses_pie_chart).grid(row=4, column=1)
Button(root, text="Line Chart", command=visualize_expenses_line_chart).grid(row=5, column=0)

# File I/O buttons
Button(root, text="Write to Excel", command=lambda: write_to_excel(df, "expenses.xlsx")).grid(row=6, column=0)
Button(root, text="Write to JSON", command=lambda: write_to_json(df, "expenses.json")).grid(row=6, column=1)

# Treeview to display expenses
tree = ttk.Treeview(root, columns=("Date", "Amount", "Category"), show='headings')
tree.heading("Date", text="Date")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.grid(row=7,columnspan=2)

# Initialize treeview with existing data from CSV
update_treeview(df)

# Start the Tkinter event loop
root.mainloop()