# Personal Finance Manager

A command-line personal finance application written in pure Python. Track expenses, generate
reports, analyse spending patterns, and back up your data — all from a simple text menu.

Built as the capstone project for **Python Programming Mastery**, covering object-oriented
design, file handling, error handling, modular code organisation and unit testing.

## Features

- Add, view, search and delete expenses
- Category-wise summary with percentage shares and ASCII bar charts
- Monthly reports with totals, averages, top category and largest expense
- Full spending analysis with a month-by-month trend
- Data saved automatically to `data/expenses.csv`
- Timestamped backups and one-click restore
- JSON export and saveable text reports
- Validation and friendly error messages on every input — the app never crashes on bad data

## Requirements

- Python 3.8 or newer. No third-party packages needed.

## Setup and run

```bash
git clone <your-repo-url>
cd python-finance-manager
python main.py
```

Sample data is already in `data/expenses.csv`, so the reports have something to show
straight away. Delete that file to start with an empty ledger.

## Usage

```
==========================================
     PERSONAL FINANCE MANAGER
==========================================

MAIN MENU:
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

Enter your choice (1-11): 1

ADD NEW EXPENSE:
Enter amount: 1500
Enter category (Food/Transport/Entertainment/Shopping/Bills/Health/Other): Food
Enter date (YYYY-MM-DD, blank = today): 2024-01-15
Enter description: Grocery shopping

[OK] Expense added successfully!

Press Enter to continue...
```

Type `q` at any prompt to cancel the current action and return to the menu.

## Project structure

```
python-finance-manager/
├── main.py              # entry point
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── expense.py       # Expense class
│   ├── file_manager.py  # CSV read/write, backup, restore, export
│   ├── menu.py          # command-line interface
│   ├── reports.py       # report and analysis functions
│   └── utils.py         # validation and formatting helpers
├── data/
│   ├── expenses.csv     # your data (sample included)
│   └── backups/         # timestamped backups
├── reports/             # generated report and export files
├── docs/
│   └── user_guide.md
└── tests/
    └── test_finance.py
```

## Running the tests

```bash
python -m unittest discover tests -v
```

## How it works

- `Expense` validates its own amount, category and date on creation, and converts to and from
  a dictionary for CSV storage.
- `file_manager` handles all disk access. Unreadable rows are skipped with a warning rather
  than stopping the program, and every write is wrapped in error handling.
- `reports` is pure calculation — no input, no printing side effects — which makes it easy
  to test.
- `menu` owns all user interaction and saves to disk after every change.

## Licence

MIT — free to use and modify.
