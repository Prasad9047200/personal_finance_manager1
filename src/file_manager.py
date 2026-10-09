"""CSV persistence, backup and restore, and JSON export."""

import csv
import json
import os
import shutil
from datetime import datetime

from .expense import Expense

FIELDNAMES = ["Date", "Category", "Amount", "Description"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
DATA_FILE = os.path.join(DATA_DIR, "expenses.csv")


def ensure_dirs():
    for folder in (DATA_DIR, BACKUP_DIR, REPORT_DIR):
        os.makedirs(folder, exist_ok=True)


def load_expenses(filename=DATA_FILE):
    """Read expenses from CSV. Bad rows are skipped and reported, never fatal."""
    ensure_dirs()
    expenses, skipped = [], 0
    if not os.path.exists(filename):
        return expenses
    try:
        with open(filename, "r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                try:
                    expenses.append(Expense.from_dict(row))
                except (ValueError, KeyError, TypeError):
                    skipped += 1
    except (OSError, csv.Error) as error:
        print(f"  ! Could not read {filename}: {error}")
        return []
    if skipped:
        print(f"  ! Skipped {skipped} unreadable row(s) in {os.path.basename(filename)}.")
    return expenses


def save_expenses(expenses, filename=DATA_FILE):
    """Write all expenses to CSV. Returns True on success."""
    ensure_dirs()
    try:
        with open(filename, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense.to_dict())
        return True
    except OSError as error:
        print(f"  ! Could not save data: {error}")
        return False


def backup_data(filename=DATA_FILE):
    """Copy the data file into data/backups with a timestamped name."""
    ensure_dirs()
    if not os.path.exists(filename):
        print("  ! Nothing to back up yet.")
        return None
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = os.path.join(BACKUP_DIR, f"expenses_{stamp}.csv")
    try:
        shutil.copyfile(filename, target)
        return target
    except OSError as error:
        print(f"  ! Backup failed: {error}")
        return None


def list_backups():
    ensure_dirs()
    try:
        names = sorted(n for n in os.listdir(BACKUP_DIR) if n.endswith(".csv"))
    except OSError:
        return []
    return [os.path.join(BACKUP_DIR, n) for n in names]


def restore_backup(path, filename=DATA_FILE):
    """Replace the live data file with a backup copy."""
    try:
        shutil.copyfile(path, filename)
        return True
    except OSError as error:
        print(f"  ! Restore failed: {error}")
        return False


def export_json(expenses, filename=None):
    ensure_dirs()
    filename = filename or os.path.join(
        REPORT_DIR, f"expenses_{datetime.now():%Y%m%d_%H%M%S}.json"
    )
    try:
        with open(filename, "w", encoding="utf-8") as handle:
            json.dump([e.to_dict() for e in expenses], handle, indent=2)
        return filename
    except OSError as error:
        print(f"  ! Export failed: {error}")
        return None


def write_report(text, prefix="report"):
    ensure_dirs()
    path = os.path.join(REPORT_DIR, f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.txt")
    try:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path
    except OSError as error:
        print(f"  ! Could not write report: {error}")
        return None
