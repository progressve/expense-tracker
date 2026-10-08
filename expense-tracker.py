import mysql.connector
from datetime import datetime
from tkinter import *
from tkinter import messagebox

pwd=""

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=pwd,
        database="expense_db"
    )

def create():
    conn = mysql.connector.connect(host="localhost", user="root", password=pwd)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_db")
    conn.close()

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        amount DECIMAL(10,2),
        category VARCHAR(255),
        description VARCHAR(255),
        date DATE
    )
    """)
    conn.commit()
    conn.close()

def load_categories():
    global cat
    try:
        with open("cats.txt", "r") as f:
            cat = [line.strip() for line in f.readlines() if line.strip()]
        if not cat:
            cat = ['Lifestyle', 'Tax', 'Services', 'Miscellaneous']
            save_categories()
    except FileNotFoundError:
        cat = ['Lifestyle', 'Tax', 'Services', 'Miscellaneous']
        save_categories()
def save_categories():
    with open("cats.txt", "w") as f:
        for c in cat:
            f.write(c + "\n")
load_categories()

def logs(message):
    with open("expense_log.txt", "a") as file:
        file.write(f"{datetime.now()} - {message}\n")

def add():
    try:
        amt = amount.get()
        cat_val = category.get()
        descr = desc.get()
        date = datetime.today().strftime('%Y-%m-%d')

        if not amt or not cat_val or not descr:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (%s,%s,%s,%s)",
            (float(amt), cat_val, descr, date)
        )
        conn.commit()
        conn.close()
        if cat_val not in cat:
            cat.append(cat_val)
            save_categories()
        logs(f"Added: {amt} | {cat_val} | {descr} | {date}")
        messagebox.showinfo("Success", "Expense added")
        clear()
        load()
        cats.set("Current Categories: " + ", ".join(cat))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def load(cat_val=None):
    expenses.delete(0, END)
    conn = connect()
    cursor = conn.cursor()
    if cat_val:
        cursor.execute("SELECT * FROM expenses WHERE category=%s ORDER BY date DESC", (cat_val,))
    else:
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    records = cursor.fetchall()
    conn.close()

    for r in records:
        expenses.insert(END, f"ID:{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")

def delete():
    selected = expenses.curselection()
    if not selected:
        messagebox.showwarning("Select", "Select an expense to delete")
        return
    val = expenses.get(selected)
    ide = int(val.split("|")[0].split(":")[1])

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=%s", (ide,))
    conn.commit()
    conn.close()

    logs(f"Deleted expense ID {ide}")
    load()
    messagebox.showinfo("Deleted", f"Expense ID {ide} deleted")

def sortCategory():
    filter_val = filter.get()
    if not filter_val:
        messagebox.showwarning("Input", "Enter category to filter")
        return
    load(filter_val)

def clear():
    amount.delete(0, END)
    category.delete(0, END)
    desc.delete(0, END)

create()
root = Tk()
root.title("Expense Tracker")
root.geometry("900x400")

# Horizontal Frame with inputs
inputFrame = Frame(root, pady=10)
inputFrame.pack(fill=X)

Label(inputFrame, text="Amount:").grid(row=0, column=0, padx=5)
amount = Entry(inputFrame, width=10)
amount.grid(row=0, column=1, padx=5)

Label(inputFrame, text="Category:").grid(row=0, column=2, padx=5)
category = Entry(inputFrame, width=15)
category.grid(row=0, column=3, padx=5)

Label(inputFrame, text="Description:").grid(row=0, column=4, padx=5)
desc = Entry(inputFrame, width=25)
desc.grid(row=0, column=5, padx=5)

Button(inputFrame, text="Add Expense", command=add).grid(row=0, column=6, padx=10)

# Show current categories
cats = StringVar()
cats.set("Current Categories: " + ", ".join(cat))
Label(root, textvariable=cats).pack(pady=5)

# Horizontal frame with functions
horFrame = Frame(root, pady=5)
horFrame.pack(fill=X)

Label(horFrame, text="Filter by Category:").grid(row=0, column=0, padx=5)
filter = Entry(horFrame, width=15)
filter.grid(row=0, column=1, padx=5)
Button(horFrame, text="Filter", command=sortCategory).grid(row=0, column=2, padx=5)
Button(horFrame, text="Show All", command=lambda: load()).grid(row=0, column=3, padx=5)

# Expenses List
expenses = Listbox(root, width=120)
expenses.pack(pady=10, fill=BOTH, expand=True)

Button(root, text="Delete Selected", command=delete).pack(pady=5)

load()
root.mainloop()
