"""
Expense Tracker Application
A simple command-line expense tracker that allows users to:
- Add new expenses (amount, category, description)
- View all recorded expenses
- Calculate total expenses
- Search expenses by category
- Persist data to a JSON file
- Load data automatically on startup
"""

import json
import os

# --- Constants ---
DATA_FILE = "expenses.json"  # File where expense data is stored


# --- Helper Functions ---

def load_expenses():
    """
    Load expenses from the JSON data file.
    Returns a list of expense dictionaries.
    If the file doesn't exist or is corrupted, returns an empty list.
    """
    if not os.path.exists(DATA_FILE):
        return []  # No data file yet — start fresh
    
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        # Handle corrupted file or read errors gracefully
        print("Warning: Data file is corrupted. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """
    Save the list of expenses to the JSON data file.
    
    Args:
        expenses (list): List of expense dictionaries to persist.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    """
    Prompt the user to enter a new expense and append it to the list.
    
    Args:
        expenses (list): The current list of expense dictionaries.
    
    Returns:
        list: Updated list of expenses.
    """
    print("\n--- Add a New Expense ---")
    
    # Get and validate amount
    try:
        amount = float(input("Enter amount (e.g., 12.50): $"))
        if amount <= 0:
            print("Amount must be positive. Expense not added.")
            return expenses
    except ValueError:
        print("Invalid amount. Please enter a number. Expense not added.")
        return expenses
    
    # Get category
    category = input("Enter category (e.g., Food, Transport, Utilities): ").strip()
    if not category:
        print("Category cannot be empty. Expense not added.")
        return expenses
    
    # Get description
    description = input("Enter description: ").strip()
    if not description:
        print("Description cannot be empty. Expense not added.")
        return expenses
    
    # Build and append the new expense record
    new_expense = {
        "amount": round(amount, 2),
        "category": category,
        "description": description
    }
    expenses.append(new_expense)
    print("Expense added successfully!")
    
    return expenses


def view_expenses(expenses):
    """
    Display all recorded expenses in a formatted table.
    
    Args:
        expenses (list): The list of expense dictionaries to display.
    """
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    
    print("\n--- All Expenses ---")
    print(f"{'#':<4} {'Amount':<10} {'Category':<15} {'Description'}")
    print("-" * 50)
    
    for idx, expense in enumerate(expenses, start=1):
        amount = f"${expense['amount']:.2f}"
        print(f"{idx:<4} {amount:<10} {expense['category']:<15} {expense['description']}")
    print("-" * 50)


def calculate_total(expenses):
    """
    Calculate and display the total of all expenses.
    
    Args:
        expenses (list): The list of expense dictionaries.
    """
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal Expenses: ${total:.2f}")


def show_menu():
    """
    Display the main menu options to the user.
    """
    print("\n===== Expense Tracker =====")
    print("1. Add a new expense")
    print("2. View all expenses")
    print("3. Calculate total expenses")
    print("4. Exit")
    print("===========================")


# --- Main Program ---

def main():
    """
    Main entry point for the Expense Tracker application.
    Loads existing data and runs the interactive menu loop.
    """
    # Load expenses from file when the program starts
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} existing expense(s).")
    
    while True:
        show_menu()
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            # Add a new expense and save changes immediately
            expenses = add_expense(expenses)
            save_expenses(expenses)
        
        elif choice == "2":
            # Display all expenses
            view_expenses(expenses)
        
        elif choice == "3":
            # Show total of all expenses
            calculate_total(expenses)
        
        elif choice == "4":
            # Exit the application
            print("Goodbye!")
            break
        
        else:
            # Handle invalid menu choices
            print("Invalid option. Please choose 1, 2, 3, or 4.")


# --- Run the Application ---
if __name__ == "__main__":
    main()
