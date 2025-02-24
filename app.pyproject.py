import pandas as pd
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename="expenses.csv"):
        """Initialize the filename and check if it exists, otherwise create one."""
        self.filename = filename
        try:
            self.df = pd.read_csv(self.filename)
        except FileNotFoundError:
            # If the file doesn't exist, create a new dataframe with columns for the expense entries.
            self.df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
            self.df.to_csv(self.filename, index=False)

    def log_expense(self, category, description, amount):
        """Log a new expense into the CSV file."""
        new_expense = {.
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Category": category,
            "Description": description,
            "Amount": amount
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_expense])], ignore_index=True)
        self.df.to_csv(self.filename, index=False)
        print("Expense logged successfully!")

    def analyze_expenses(self, start_date=None, end_date=None):
        """Analyze the total expenses between the specified date range (optional)."""
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df = self.df[self.df['Date'] >= start_date]
        
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            self.df = self.df[self.df['Date'] <= end_date]
        
        total_expenses = self.df['Amount'].sum()
        print(f"Total Expenses: ${total_expenses:.2f}")
        
        # Grouping expenses by category to get an overview
        category_summary = self.df.groupby('Category').agg({'Amount': 'sum'}).reset_index()
        print("\nExpenses by Category:")
        print(category_summary)
        
        return total_expenses, category_summary

    def show_expenses(self):
        """Show all logged expenses."""
        print(self.df)

# Example Usage:
tracker = ExpenseTracker()

# Log some expenses
tracker.log_expense("Food", "Lunch at Cafe", 12.50)
tracker.log_expense("Transport", "Taxi Ride", 25.00)
tracker.log_expense("Food", "Grocery Shopping", 30.00)

# Analyze expenses between dates
tracker.analyze_expenses(start_date="2025-02-20", end_date="2025-02-24")

# Show all expenses
tracker.show_expenses()
