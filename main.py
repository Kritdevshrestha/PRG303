from tkinter import *
from tkinter import ttk
root = Tk()
root.title("Krittracker")

def add_expense():
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

            # Update tree view (optional)
            tree.insert("", "end", values=(date, amount, category))

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")


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

# Button to visualize expenses
Button(root, text="Visualize Expenses").grid(row=5,columnspan=2)

# Treeview to display expenses
tree = ttk.Treeview(root, columns=("Date", "Amount", "Category"), show='headings')
tree.heading("Date", text="Date")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.grid(row=4,columnspan=2)

# Start the Tkinter event loop
root.mainloop()