import csv
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from expense_tracker import load_expenses, save_expenses, month_total, load_budgets, save_budgets


class ExpenseTrackerTests(unittest.TestCase):
    def test_csv_round_trip_and_month_total(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.csv"
            records = [
                {"date": "2026-11-02", "category": "Food", "amount": Decimal("120.50"), "description": "Lunch"},
                {"date": "2026-10-31", "category": "Travel", "amount": Decimal("50"), "description": "Bus"},
            ]
            save_expenses(records, path)
            loaded = load_expenses(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(month_total(loaded, "2026-11"), Decimal("120.50"))

    def test_invalid_csv_rows_are_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expenses.csv"
            path.write_text("date,category,amount,description\nnot-a-date,Food,10,x\n2026-11-01,Food,-2,x\n", encoding="utf-8")
            self.assertEqual(load_expenses(path), [])

    def test_budgets_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "budgets.json"
            save_budgets({"2026-11": Decimal("1000")}, path)
            self.assertEqual(load_budgets(path)["2026-11"], Decimal("1000"))


if __name__ == "__main__":
    unittest.main()
