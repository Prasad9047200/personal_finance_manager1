"""Utility functions: input validation, formatting and safe prompts."""

from datetime import datetime

from .expense import CATEGORIES


def format_currency(value):
    """Format a number as Indian rupees with thousands separators."""
    return f"Rs.{float(value):,.2f}"


def validate_amount(text):
    """Return a positive float or raise ValueError with a friendly message."""
    try:
        amount = float(str(text).replace(",", "").strip())
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number, e.g. 1500 or 249.50")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if amount > 10_000_000:
        raise ValueError("Amount looks too large. Please check and try again.")
    return round(amount, 2)


def validate_date(text):
    """Return a YYYY-MM-DD string or raise ValueError."""
    text = str(text).strip()
    if not text:
        return datetime.today().strftime("%Y-%m-%d")
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must look like YYYY-MM-DD, e.g. 2024-01-15")
    if parsed > datetime.today():
        raise ValueError("Date cannot be in the future.")
    return parsed.strftime("%Y-%m-%d")


def validate_category(text):
    """Match the typed category against the known list (case-insensitive)."""
    text = str(text).strip()
    if not text:
        return "Other"
    for category in CATEGORIES:
        if category.lower() == text.lower():
            return category
    raise ValueError("Category must be one of: " + ", ".join(CATEGORIES))


def validate_month(text):
    """Return a YYYY-MM string or raise ValueError."""
    text = str(text).strip()
    if not text:
        return datetime.today().strftime("%Y-%m")
    try:
        datetime.strptime(text, "%Y-%m")
    except ValueError:
        raise ValueError("Month must look like YYYY-MM, e.g. 2024-01")
    return text


def prompt(message, validator=None, allow_blank=False):
    """Ask the user until the answer passes the validator. Returns None if cancelled."""
    while True:
        try:
            answer = input(message).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return None
        if answer.lower() in {"q", "cancel"}:
            print("Cancelled.")
            return None
        if not answer and allow_blank:
            return ""
        if validator is None:
            if answer or allow_blank:
                return answer
            print("  ! This field cannot be empty. (type q to cancel)")
            continue
        try:
            return validator(answer)
        except ValueError as error:
            print(f"  ! {error} (type q to cancel)")


def pause():
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        print()
