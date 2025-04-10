# L7-INFORMATICS-TEST

Budget Buddy

Budget Buddy is a simple and interactive Streamlit app to track your daily expenses, manage monthly budgets, and get visual feedback on your spending habits — all in one place.

## Features

- Add and categorize expenses easily
- Set monthly budgets per category
- Visual summary of expenses and budget progress
- Custom alerts when you're about to exceed your budget (for example, when only 10% remains)
- Clean and responsive UI with auto-sorting of expenses

---

## Requirements

Make sure you have Python 3.8 or higher installed.

Install the required packages:

```bash
pip install streamlit pandas
````

Running the App
Clone this repository (or save the script in a .py file):
git clone https://github.com/yourusername/budget-buddy.git
cd budget-buddy

Run the Streamlit application:
streamlit run app.py

Replace app.py with the filename if it's different.

Your default web browser will open the app at:
http://localhost:8501

How to Use
Add Expenses

Select the date, category, amount, and an optional description.

Click "Add Expense" to record it.

Set Budgets

Use the budget section to define your monthly spending limit per category.

View Summary

Check real-time feedback on how much you've spent versus your budget.

Receive an alert if you're nearing your budget threshold.

Expense Table

Review all your transactions for the current month in a sortable table.

Project Structure

budget-buddy/
├── app.py               # Main Streamlit application
├── README.md            # This file

Notes
Data is stored temporarily using Streamlit session state (not saved after the app closes).

No database or internet connection is required.

This app is ideal for individual use and budget tracking demos.
