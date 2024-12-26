# Personal Finance Tracker

import json
from datetime import datetime

# Welcome message
print("Welcome to your Personal Finance Tracker!")
print("Track your spending, manage your budget, and take control of your finances.")

# Global list to store transactions
transactions = [
    {"date": "2024-12-20", "category": "Groceries", "amount": 45.67, "description": "Supermarket shopping"},
    {"date": "2024-12-19", "category": "Entertainment", "amount": 15.00, "description": "Movie night"},
    {"date": "2024-12-18", "category": "Transportation", "amount": 25.50, "description": "Monthly bus pass"},
    {"date": "2024-12-17", "category": "Dining Out", "amount": 30.00, "description": "Dinner with friends"},
    {"date": "2024-12-16", "category": "Health", "amount": 60.00, "description": "Pharmacy supplies"},
    {"date": "2024-12-15", "category": "Shopping", "amount": 120.00, "description": "Clothing purchase"},
    {"date": "2024-12-14", "category": "Utilities", "amount": 80.00, "description": "Electricity bill"},
    {"date": "2024-12-13", "category": "Groceries", "amount": 55.25, "description": "Weekly grocery run"},
    {"date": "2024-12-12", "category": "Education", "amount": 200.00, "description": "Online course subscription"},
    {"date": "2024-12-11", "category": "Entertainment", "amount": 50.00, "description": "Concert tickets"}
]

# Load transactions from a file
def load_transactions(filename="transactions.json"):
    try:
        with open(filename, "r") as file:
            global transactions
            transactions = json.load(file)
    except FileNotFoundError:
        print("No previous records found. Starting with sample data!")

def save_transactions(filename="transactions.json"):
    with open(filename, "w") as file:
        json.dump(transactions, file, indent=4)
    print("Your transactions have been saved successfully.")

# Add a new transaction
def add_transaction(date, category, amount, description):
    transactions.append({
        "date": date,
        "category": category,
        "amount": float(amount),
        "description": description
    })
    save_transactions()
    print("Transaction added successfully! Great job keeping track.")

# Remove a transaction by index
def remove_transaction(index):
    try:
        removed = transactions.pop(index)
        save_transactions()
        print(f"Removed transaction: {removed}. Goodbye unnecessary expense!")
    except IndexError:
        print("Oops! That index doesn't exist. Try again.")

# Edit a transaction by index
def edit_transaction(index, date=None, category=None, amount=None, description=None):
    try:
        if date:
            transactions[index]["date"] = date
        if category:
            transactions[index]["category"] = category
        if amount:
            transactions[index]["amount"] = float(amount)
        if description:
            transactions[index]["description"] = description
        save_transactions()
        print("Transaction updated successfully! Changes saved.")
    except IndexError:
        print("Oops! That index doesn't exist. Try again.")

# Summarize transactions by category or time range
def summarize_transactions(by="category"):
    summary = {}
    if by == "category":
        for transaction in transactions:
            category = transaction["category"]
            summary[category] = summary.get(category, 0) + transaction["amount"]
    elif by == "date_range":
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            for transaction in transactions:
                t_date = datetime.strptime(transaction["date"], "%Y-%m-%d")
                if start_date <= t_date <= end_date:
                    summary[transaction["date"]] = summary.get(transaction["date"], 0) + transaction["amount"]
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    print("\nHere is your summarized report:")
    for key, total in summary.items():
        print(f"{key}: ${total:.2f}")

# Display all transactions
def display_transactions():
    if not transactions:
        print("No transactions to display yet. Start adding your expenses!")
        return
    print("\nHere are all your transactions:")
    for idx, transaction in enumerate(transactions):
        print(f"[{idx}] {transaction['date']} - {transaction['category']} - ${transaction['amount']:.2f} - {transaction['description']}")

# Command-line menu
def menu():
    while True:
        print("\n=== Personal Finance Tracker Menu ===")
        print("1. Add Transaction")
        print("2. Remove Transaction")
        print("3. Edit Transaction")
        print("4. Display Transactions")
        print("5. Summarize Transactions")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\nLet's add a new transaction:")
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = input("Enter amount: ")
            description = input("Enter description: ")
            add_transaction(date, category, amount, description)
        elif choice == "2":
            display_transactions()
            index = int(input("Enter the index of the transaction to remove: "))
            remove_transaction(index)
        elif choice == "3":
            display_transactions()
            index = int(input("Enter the index of the transaction to edit: "))
            date = input("Enter new date (leave blank to keep current): ") or None
            category = input("Enter new category (leave blank to keep current): ") or None
            amount = input("Enter new amount (leave blank to keep current): ") or None
            description = input("Enter new description (leave blank to keep current): ") or None
            edit_transaction(index, date, category, amount, description)
        elif choice == "4":
            display_transactions()
        elif choice == "5":
            summarize_transactions()
        elif choice == "6":
            print("Thanks for using the Personal Finance Tracker! See you next time.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    load_transactions()
    menu()
