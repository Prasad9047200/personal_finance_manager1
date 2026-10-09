"""Report generation: totals, averages, category summaries and monthly trends."""

from collections import defaultdict

from .utils import format_currency

LINE = "=" * 58


def total(expenses):
    return sum(e.amount for e in expenses)


def average(expenses):
    return total(expenses) / len(expenses) if expenses else 0.0


def by_category(expenses):
    """Return {category: total} sorted from highest to lowest."""
    buckets = defaultdict(float)
    for expense in expenses:
        buckets[expense.category] += expense.amount
    return dict(sorted(buckets.items(), key=lambda item: item[1], reverse=True))


def by_month(expenses):
    buckets = defaultdict(float)
    for expense in expenses:
        buckets[expense.month] += expense.amount
    return dict(sorted(buckets.items()))


def filter_month(expenses, month):
    return [e for e in expenses if e.month == month]


def search(expenses, term):
    """Case-insensitive search across category, description and date."""
    term = term.lower().strip()
    return [
        e
        for e in expenses
        if term in e.category.lower() or term in e.description.lower() or term in e.date
    ]


def _bar(value, maximum, width=24):
    if maximum <= 0:
        return ""
    return "#" * max(1, int(round(value / maximum * width)))


def category_summary(expenses):
    if not expenses:
        return "No expenses recorded yet."
    grand = total(expenses)
    buckets = by_category(expenses)
    biggest = max(buckets.values())
    lines = [LINE, "CATEGORY-WISE SUMMARY".center(58), LINE]
    for category, amount in buckets.items():
        share = amount / grand * 100
        lines.append(
            f"{category:<14} {format_currency(amount):>14}  {share:5.1f}%  {_bar(amount, biggest)}"
        )
    lines += [LINE, f"{'TOTAL':<14} {format_currency(grand):>14}", LINE]
    return "\n".join(lines)


def monthly_report(expenses, month):
    rows = filter_month(expenses, month)
    lines = [LINE, f"MONTHLY REPORT - {month}".center(58), LINE]
    if not rows:
        lines.append("No expenses recorded for this month.")
        lines.append(LINE)
        return "\n".join(lines)
    for expense in sorted(rows, key=lambda e: e.date):
        lines.append(str(expense))
    highest = max(rows, key=lambda e: e.amount)
    top_category = next(iter(by_category(rows)))
    lines += [
        LINE,
        f"Entries        : {len(rows)}",
        f"Total spent    : {format_currency(total(rows))}",
        f"Average spend  : {format_currency(average(rows))}",
        f"Top category   : {top_category}",
        f"Largest expense: {format_currency(highest.amount)} ({highest.description or highest.category})",
        LINE,
    ]
    return "\n".join(lines)


def overview(expenses):
    """A full analysis: overall stats, categories and month-by-month trend."""
    if not expenses:
        return "No expenses recorded yet."
    lines = [LINE, "SPENDING ANALYSIS".center(58), LINE]
    lines.append(f"Entries       : {len(expenses)}")
    lines.append(f"Total spent   : {format_currency(total(expenses))}")
    lines.append(f"Average spend : {format_currency(average(expenses))}")
    dates = sorted(e.date for e in expenses)
    lines.append(f"Date range    : {dates[0]} to {dates[-1]}")
    lines.append("")
    lines.append(category_summary(expenses))
    lines.append("")
    months = by_month(expenses)
    biggest = max(months.values())
    lines += [LINE, "MONTHLY TREND".center(58), LINE]
    for month, amount in months.items():
        lines.append(f"{month}   {format_currency(amount):>14}  {_bar(amount, biggest)}")
    lines.append(LINE)
    return "\n".join(lines)


def table(expenses):
    if not expenses:
        return "No expenses to show."
    lines = [LINE, f"{'DATE':<12} {'CATEGORY':<14} {'AMOUNT':>13}  DESCRIPTION", LINE]
    for expense in sorted(expenses, key=lambda e: e.date):
        lines.append(
            f"{expense.date:<12} {expense.category:<14} "
            f"{format_currency(expense.amount):>13}  {expense.description}"
        )
    lines += [LINE, f"{len(expenses)} entries · Total {format_currency(total(expenses))}", LINE]
    return "\n".join(lines)
