"""A small, CSV-backed personal expense tracker.

Run with: python expense_tracker.py
The CSV and budget JSON files are stored beside this script.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "expenses.csv"
BUDGET_FILE = BASE_DIR / "budgets.json"
FIELDS = ["date", "category", "amount", "description"]


def load_expenses(path: Path = DATA_FILE) -> list[dict]:
    """Load valid expense rows; skip malformed rows without stopping the app."""
    if not path.exists():
        return []
    expenses = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            try:
                parsed_date = date.fromisoformat(row["date"])
                amount = Decimal(row["amount"])
                category = row["category"].strip()
                if amount <= 0 or not category:
                    continue
                expenses.append({
                    "date": parsed_date.isoformat(),
                    "category": category,
                    "amount": amount,
                    "description": (row.get("description") or "").strip(),
                })
            except (KeyError, ValueError, InvalidOperation, TypeError):
                continue
    return expenses


def save_expenses(expenses: list[dict], path: Path = DATA_FILE) -> None:
    """Persist expenses in a stable CSV format."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for item in expenses:
            writer.writerow({**item, "amount": f"{Decimal(item['amount']):.2f}"})


def load_budgets(path: Path = BUDGET_FILE) -> dict[str, Decimal]:
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return {key: Decimal(value) for key, value in raw.items()}
    except (json.JSONDecodeError, InvalidOperation, AttributeError):
        return {}


def save_budgets(budgets: dict[str, Decimal], path: Path = BUDGET_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {month: str(amount) for month, amount in budgets.items()}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def month_total(expenses: list[dict], month: str) -> Decimal:
    return sum(
        (Decimal(item["amount"]) for item in expenses if item["date"].startswith(month)),
        start=Decimal("0"),
    )


def add_expense(expenses: list[dict]) -> None:
    try:
        expense_date = date.fromisoformat(input("Date (YYYY-MM-DD): ").strip())
        category = input("Category: ").strip()
        amount = Decimal(input("Amount: ").strip())
        description = input("Description: ").strip()
        if not category or amount <= 0:
            raise ValueError("Category is required and amount must be positive.")
    except (ValueError, InvalidOperation):
        print("Invalid input. Please check the date, category and positive amount.")
        return
    expenses.append({
        "date": expense_date.isoformat(),
        "category": category,
        "amount": amount,
        "description": description,
    })
    print("Expense added.")


def show_expenses(expenses: list[dict], month: str | None = None) -> None:
    selected = [item for item in expenses if month is None or item["date"].startswith(month)]
    if not selected:
        print("No expenses found.")
        return
    print("\nDate       | Category       | Amount   | Description")
    print("-" * 68)
    for item in sorted(selected, key=lambda row: row["date"]):
        print(f"{item['date']} | {item['category'][:14]:14} | {Decimal(item['amount']):8.2f} | {item['description']}")
    print(f"Total: {sum((Decimal(item['amount']) for item in selected), Decimal('0')):.2f}")


def main() -> None:
    expenses = load_expenses()
    budgets = load_budgets()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense  2. View all  3. Monthly summary")
        print("4. Set monthly budget  5. Exit")
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
            save_expenses(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            month = input("Month (YYYY-MM): ").strip()
            try:
                datetime.strptime(month, "%Y-%m")
            except ValueError:
                print("Enter month as YYYY-MM.")
                continue
            total = month_total(expenses, month)
            budget = budgets.get(month)
            print(f"Spent in {month}: {total:.2f}")
            if budget is not None:
                print(f"Budget: {budget:.2f} | Remaining: {budget - total:.2f}")
            show_expenses(expenses, month)
        elif choice == "4":
            month = input("Month (YYYY-MM): ").strip()
            try:
                datetime.strptime(month, "%Y-%m")
                amount = Decimal(input("Budget amount: ").strip())
                if amount <= 0:
                    raise ValueError
            except (ValueError, InvalidOperation):
                print("Enter a valid month and positive budget.")
                continue
            budgets[month] = amount
            save_budgets(budgets)
            print("Budget saved.")
        elif choice == "5":
            save_expenses(expenses)
            save_budgets(budgets)
            print("Saved. Goodbye!")
            break
        else:
            print("Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
