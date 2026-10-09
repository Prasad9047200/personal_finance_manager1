# User Guide

## Getting started

1. Install Python 3.8 or newer from python.org.
2. Open a terminal in the project folder.
3. Run `python main.py`.

The menu appears with a running count of your expenses and total spend at the top.

## Menu options explained

| Option | What it does |
| --- | --- |
| 1. Add New Expense | Asks for amount, category, date and description. Blank date means today. |
| 2. View All Expenses | A table of every expense, oldest first, with the total at the bottom. |
| 3. Category-wise Summary | Totals per category with percentage shares and bar charts. |
| 4. Generate Monthly Report | Enter a month like `2024-01`. Offers to save the report to `reports/`. |
| 5. Search Expenses | Matches text against category, description or date. |
| 6. Delete an Expense | Lists numbered entries, asks which to remove, then confirms. |
| 7. Spending Analysis | Overall stats, category breakdown and month-by-month trend. |
| 8. Export Data | Writes a JSON copy of all expenses into `reports/`. |
| 9. Backup Data | Saves a timestamped copy into `data/backups/`. |
| 10. Restore Backup | Pick a backup to replace the current data. Asks for confirmation. |
| 11. Exit | Saves and quits. |

Type `q` at any prompt to cancel and go back to the menu.

## Input rules

- **Amount** — a positive number. Commas are allowed (`1,500`). Letters are rejected.
- **Category** — one of Food, Transport, Entertainment, Shopping, Bills, Health, Other.
  Case does not matter. Blank becomes `Other`.
- **Date** — `YYYY-MM-DD`. Future dates are rejected. Blank becomes today.
- **Month** — `YYYY-MM`. Blank becomes the current month.
- **Description** — any text, may be left blank.

If an entry is invalid the app explains what went wrong and asks again. Nothing is lost.

## Where your data lives

- `data/expenses.csv` — your live data, updated after every change.
- `data/backups/expenses_YYYYMMDD_HHMMSS.csv` — backup copies.
- `reports/` — saved text reports and JSON exports.

The CSV is a plain text file you can open in Excel or Google Sheets. Keep the header row
`Date,Category,Amount,Description` intact if you edit it by hand.

## Troubleshooting

**"Skipped N unreadable row(s)"** — a row in the CSV has a bad date or amount. Open the file
and fix or remove that row, or restore a backup.

**Data seems missing** — check you are running `python main.py` from the project folder;
paths are resolved relative to the project, not your current directory.

**Nothing happens on a menu choice** — enter just the number, for example `4`, then Enter.
