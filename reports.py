import sqlite3
import matplotlib.pyplot as plt


def show_category_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(7, 5))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Category-wise Expenses")
    plt.show()


def get_total_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0