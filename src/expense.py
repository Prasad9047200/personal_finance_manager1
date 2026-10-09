"""Expense class definition - the core data model of the application."""

from datetime import datetime

CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Health", "Other"]


class Expense:
    """A single expense record."""

    def __init__(self, amount, category, date, description=""):
        self.amount = float(amount)
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.category = str(category).strip().title()
        self.date = self._parse_date(date)
        self.description = str(description).strip()

    @staticmethod
    def _parse_date(value):
        """Accept a date string (YYYY-MM-DD) or a date object, return YYYY-MM-DD string."""
        if hasattr(value, "strftime"):
            return value.strftime("%Y-%m-%d")
        value = str(value).strip()
        datetime.strptime(value, "%Y-%m-%d")  # raises ValueError if invalid
        return value

    @property
    def month(self):
        """Return the YYYY-MM month key for this expense."""
        return self.date[:7]

    def to_dict(self):
        return {
            "Date": self.date,
            "Category": self.category,
            "Amount": f"{self.amount:.2f}",
            "Description": self.description,
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            amount=row["Amount"],
            category=row["Category"],
            date=row["Date"],
            description=row.get("Description", ""),
        )

    def __str__(self):
        return f"{self.date} | {self.category:<14} | Rs.{self.amount:>10,.2f} | {self.description}"

    def __repr__(self):
        return f"Expense({self.amount!r}, {self.category!r}, {self.date!r}, {self.description!r})"

    def __eq__(self, other):
        return isinstance(other, Expense) and self.to_dict() == other.to_dict()
