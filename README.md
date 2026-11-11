# Personal Expense Tracker

A lightweight Python CLI application for recording expenses, reviewing monthly spending and tracking month-specific budgets. Built with Python's standard library; no third-party packages are required.

## Features
- Add expenses with ISO dates, category, positive amount and description.
- Persist transactions in a CSV file.
- Store a separate budget for each month in JSON.
- View all transactions or a selected month's transactions and total.
- Validate user input and skip malformed CSV rows rather than crashing.

## Requirements
- Python 3.10 or newer
- No external dependencies

## Run locally
```bash
git clone https://github.com/Jayendracoder/Personal-expense-tracker-by-jayendra.git
cd Personal-expense-tracker-by-jayendra
python expense_tracker.py
```

The application creates `expenses.csv` and `budgets.json` beside the script when data is saved. These are local user data files and should not be committed.

## Data format
- `expenses.csv`: `date, category, amount, description`
- `budgets.json`: mapping of `YYYY-MM` to a positive budget amount

## Project structure
```text
.
├── expense_tracker.py
├── tests/
│   └── test_expense_tracker.py
├── .gitignore
└── README.md
```

## Scope and limitations
This is a local, single-user command-line project. It does not provide authentication, cloud sync, bank integrations or financial advice. Currency is displayed as a plain numeric amount; choose and use one currency consistently in your own records.

## Roadmap
- Add automated tests and continuous integration.
- Add category summaries and export options.
- Consider a Streamlit interface after the core data model is tested.

## Author
Jayendra Karke · [GitHub](https://github.com/Jayendracoder)
