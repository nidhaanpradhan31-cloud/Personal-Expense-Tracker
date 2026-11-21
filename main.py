import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import create_database
from expense import (
    add_expense,
    get_expenses,
    delete_expense,
    update_expense
)
from reports import show_category_chart, get_total_expense


# Create database
create_database()


# ----------------------------
# ADD EXPENSE
# ----------------------------

def add_new_expense():

    expense_date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if category == "" or amount == "":
        messagebox.showwarning(
            "Warning",
            "Please enter category and amount."
        )
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )
        return

    add_expense(
        expense_date,
        category,
        amount,
        description
    )

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    load_expenses()
    update_total()


# ----------------------------
# LOAD EXPENSES
# ----------------------------

def load_expenses():

    for item in expense_table.get_children():
        expense_table.delete(item)

    expenses = get_expenses()

    for expense in expenses:
        expense_table.insert(
            "",
            tk.END,
            values=expense
        )


# ----------------------------
# DELETE EXPENSE
# ----------------------------

def delete_selected_expense():

    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense."
        )
        return

    values = expense_table.item(
        selected[0]
    )["values"]

    expense_id = values[0]

    delete_expense(expense_id)

    messagebox.showinfo(
        "Success",
        "Expense deleted successfully!"
    )

    load_expenses()
    update_total()


# ----------------------------
# EDIT EXPENSE
# ----------------------------

def edit_expense():

    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense."
        )
        return

    values = expense_table.item(
        selected[0]
    )["values"]

    expense_id = values[0]

    expense_date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )
        return

    update_expense(
        expense_id,
        expense_date,
        category,
        amount,
        description
    )

    messagebox.showinfo(
        "Success",
        "Expense updated successfully!"
    )

    load_expenses()
    update_total()


# ----------------------------
# SELECT EXPENSE
# ----------------------------

def select_expense(event):

    selected = expense_table.selection()

    if not selected:
        return

    values = expense_table.item(
        selected[0]
    )["values"]

    date_entry.delete(0, tk.END)
    date_entry.insert(0, values[1])

    category_var.set(values[2])

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, values[3])

    description_entry.delete(0, tk.END)
    description_entry.insert(0, values[4])


# ----------------------------
# UPDATE TOTAL
# ----------------------------

def update_total():

    total = get_total_expense()

    total_label.config(
        text=f"Total Expense: ₹ {total:.2f}"
    )


# ----------------------------
# SHOW GRAPH
# ----------------------------

def show_graph():
    show_category_chart()


# ----------------------------
# MAIN WINDOW
# ----------------------------

root = tk.Tk()

root.title("Personal Expense Tracker")

root.geometry("900x600")


# ----------------------------
# TITLE
# ----------------------------

title_label = tk.Label(
    root,
    text="PERSONAL EXPENSE TRACKER",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=15)


# ----------------------------
# FORM
# ----------------------------

form_frame = tk.Frame(root)

form_frame.pack(pady=10)


tk.Label(
    form_frame,
    text="Date:"
).grid(row=0, column=0, padx=10, pady=8)

date_entry = tk.Entry(
    form_frame,
    width=20
)

date_entry.grid(
    row=0,
    column=1
)

date_entry.insert(
    0,
    date.today().strftime("%Y-%m-%d")
)


tk.Label(
    form_frame,
    text="Category:"
).grid(row=1, column=0, padx=10, pady=8)

category_var = tk.StringVar()

category_box = ttk.Combobox(
    form_frame,
    textvariable=category_var,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Bills",
        "Other"
    ],
    width=18
)

category_box.grid(
    row=1,
    column=1
)


tk.Label(
    form_frame,
    text="Amount:"
).grid(row=2, column=0, padx=10, pady=8)

amount_entry = tk.Entry(
    form_frame,
    width=20
)

amount_entry.grid(
    row=2,
    column=1
)


tk.Label(
    form_frame,
    text="Description:"
).grid(row=3, column=0, padx=10, pady=8)

description_entry = tk.Entry(
    form_frame,
    width=20
)

description_entry.grid(
    row=3,
    column=1
)


# ----------------------------
# BUTTONS
# ----------------------------

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Add Expense",
    width=15,
    command=add_new_expense
).grid(row=0, column=0, padx=5)


tk.Button(
    button_frame,
    text="Edit Expense",
    width=15,
    command=edit_expense
).grid(row=0, column=1, padx=5)


tk.Button(
    button_frame,
    text="Delete Expense",
    width=15,
    command=delete_selected_expense
).grid(row=0, column=2, padx=5)


tk.Button(
    button_frame,
    text="Show Chart",
    width=15,
    command=show_graph
).grid(row=0, column=3, padx=5)


# ----------------------------
# TOTAL
# ----------------------------

total_label = tk.Label(
    root,
    text="Total Expense: ₹ 0",
    font=("Arial", 14, "bold")
)

total_label.pack(pady=10)


# ----------------------------
# EXPENSE TABLE
# ----------------------------

columns = (
    "ID",
    "Date",
    "Category",
    "Amount",
    "Description"
)

expense_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=10
)

for column in columns:
    expense_table.heading(
        column,
        text=column
    )

    expense_table.column(
        column,
        width=150
    )

expense_table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


expense_table.bind(
    "<<TreeviewSelect>>",
    select_expense
)


# ----------------------------
# START APPLICATION
# ----------------------------

load_expenses()
update_total()

root.mainloop()