"""Interactive command-line interface."""

import os

from . import file_manager as fm
from . import reports
from .expense import CATEGORIES, Expense
from .utils import (
    format_currency,
    pause,
    prompt,
    validate_amount,
    validate_category,
    validate_date,
    validate_month,
)

HEADER = """
==========================================
     PERSONAL FINANCE MANAGER
==========================================
"""

MENU = """MAIN MENU:
1. Add New Expense
2. View All Expenses
3. View Category-wise Summary
4. Generate Monthly Report
5. Search Expenses
6. Delete an Expense
7. Spending Analysis
8. Export Data (JSON)
9. Backup Data
10. Restore Backup
11. Exit
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


class FinanceApp:
    """Holds the expense list in memory and saves after every change."""

    def __init__(self):
        self.expenses = fm.load_expenses()

    # ---------- actions ----------

    def add_expense(self):
        print("\nADD NEW EXPENSE:  (type q at any prompt to cancel)")
        amount = prompt("Enter amount: ", validate_amount)
        if amount is None:
            return
        category = prompt(
            f"Enter category ({'/'.join(CATEGORIES)}): ", validate_category, allow_blank=True
        )
        if category is None:
            return
        date = prompt("Enter date (YYYY-MM-DD, blank = today): ", validate_date, allow_blank=True)
        if date is None:
            return
        description = prompt("Enter description: ", allow_blank=True)
        if description is None:
            return
        try:
            expense = Expense(amount, category or "Other", date or None, description)
        except ValueError as error:
            print(f"  ! Could not add expense: {error}")
            return
        self.expenses.append(expense)
        if fm.save_expenses(self.expenses):
            print("\n[OK] Expense added successfully!")

    def view_all(self):
        print()
        print(reports.table(self.expenses))

    def category_summary(self):
        print()
        print(reports.category_summary(self.expenses))

    def monthly_report(self):
        month = prompt("Enter month (YYYY-MM, blank = this month): ", validate_month, allow_blank=True)
        if month is None:
            return
        text = reports.monthly_report(self.expenses, month or validate_month(""))
        print()
        print(text)
        answer = prompt("Save this report to a file? (y/n): ", allow_blank=True)
        if answer and answer.lower().startswith("y"):
            path = fm.write_report(text, prefix=f"monthly_{month}")
            if path:
                print(f"[OK] Report saved to {path}")

    def search(self):
        term = prompt("Search text (category, description or date): ")
        if term is None:
            return
        found = reports.search(self.expenses, term)
        print()
        print(reports.table(found) if found else "No matching expenses found.")

    def delete(self):
        if not self.expenses:
            print("\nNo expenses to delete.")
            return
        ordered = sorted(self.expenses, key=lambda e: e.date)
        print()
        for index, expense in enumerate(ordered, start=1):
            print(f"{index:>3}. {expense}")
        raw = prompt("\nNumber to delete: ")
        if raw is None:
            return
        try:
            index = int(raw)
            target = ordered[index - 1]
            if index < 1:
                raise IndexError
        except (ValueError, IndexError):
            print("  ! That is not a valid entry number.")
            return
        confirm = prompt(f"Delete '{target}'? (y/n): ", allow_blank=True)
        if confirm and confirm.lower().startswith("y"):
            self.expenses.remove(target)
            if fm.save_expenses(self.expenses):
                print("[OK] Expense deleted.")

    def analysis(self):
        print()
        print(reports.overview(self.expenses))

    def export(self):
        path = fm.export_json(self.expenses)
        if path:
            print(f"\n[OK] Exported {len(self.expenses)} expenses to {path}")

    def backup(self):
        path = fm.backup_data()
        if path:
            print(f"\n[OK] Backup created: {path}")

    def restore(self):
        backups = fm.list_backups()
        if not backups:
            print("\nNo backups available yet.")
            return
        print()
        for index, path in enumerate(backups, start=1):
            print(f"{index:>3}. {os.path.basename(path)}")
        raw = prompt("\nBackup number to restore: ")
        if raw is None:
            return
        try:
            chosen = backups[int(raw) - 1]
            if int(raw) < 1:
                raise IndexError
        except (ValueError, IndexError):
            print("  ! That is not a valid backup number.")
            return
        confirm = prompt("This replaces current data. Continue? (y/n): ", allow_blank=True)
        if confirm and confirm.lower().startswith("y") and fm.restore_backup(chosen):
            self.expenses = fm.load_expenses()
            print(f"[OK] Restored {len(self.expenses)} expenses.")

    # ---------- loop ----------

    def run(self):
        actions = {
            "1": self.add_expense,
            "2": self.view_all,
            "3": self.category_summary,
            "4": self.monthly_report,
            "5": self.search,
            "6": self.delete,
            "7": self.analysis,
            "8": self.export,
            "9": self.backup,
            "10": self.restore,
        }
        while True:
            clear()
            print(HEADER)
            print(
                f"Tracking {len(self.expenses)} expenses · "
                f"Total {format_currency(reports.total(self.expenses))}\n"
            )
            print(MENU)
            try:
                choice = input("Enter your choice (1-11): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return
            if choice in {"11", "q", "exit"}:
                fm.save_expenses(self.expenses)
                print("\nData saved. Goodbye!")
                return
            action = actions.get(choice)
            if not action:
                print("\n  ! Please enter a number between 1 and 11.")
                pause()
                continue
            try:
                action()
            except Exception as error:  # last-resort guard: never crash the menu
                print(f"\n  ! Unexpected problem: {error}")
            pause()
