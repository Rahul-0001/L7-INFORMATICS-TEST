import streamlit as st
import pandas as pd
from datetime import datetime


# Page Configuration

st.set_page_config(page_title="Budget Buddy", layout="centered")

# App Title and Subtitle
st.title("Budget Buddy: Expense and Savings Tracker")
st.markdown("Track your expenses and manage your monthly budget effectively.")

# Session State Initialization

# DataFrame to hold all expenses
if 'expense_data' not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(columns=["Date", "Type", "Amount", "Details"])

# Dictionary to store monthly budget for each category
if 'budget_caps' not in st.session_state:
    st.session_state.budget_caps = {}

# Keeps track of budget alerts already shown to avoid duplicate warnings
if 'notified' not in st.session_state:
    st.session_state.notified = {}

st.divider()

# Expense Input Form
st.header("Log Expense")

# Form to add new expense entry
with st.form("log_form"):
    col_left, col_right = st.columns(2)

    # Left column: Date and Category
    with col_left:
        input_date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment"])

    # Right column: Amount and Description
    with col_right:
        value = st.number_input("Amount in ₹", min_value=0.0, step=0.01, format="%.2f")
        description = st.text_input("Short Note (optional)")

    # Submit button
    save = st.form_submit_button("Save Entry")

    # On submit, add the entry to the session dataframe
    if save:
        new_row = pd.DataFrame(
            [[input_date, category, value, description]],
            columns=st.session_state.expense_data.columns
        )
        st.session_state.expense_data = pd.concat(
            [st.session_state.expense_data, new_row], ignore_index=True
        )
        st.success("Entry recorded successfully.")

st.divider()

# Budget Setup Section
st.header("Set Monthly Budget")

# Define the categories used
expense_categories = ["Food", "Transport", "Entertainment"]

# Display budget input for each category
budget_inputs = st.columns(len(expense_categories))
for idx, group in enumerate(expense_categories):
    with budget_inputs[idx]:
        st.session_state.budget_caps[group] = st.number_input(
            f"{group} Budget",
            min_value=0.0,
            value=st.session_state.budget_caps.get(group, 0.0),
            key=f"cap_{group}"
        )

st.divider()

# Monthly Overview and Alerts
st.header("Current Month Overview")

# Filter expenses to current month and year
today = datetime.today()
monthly_expenses = st.session_state.expense_data[
    (pd.to_datetime(st.session_state.expense_data["Date"]).dt.month == today.month) &
    (pd.to_datetime(st.session_state.expense_data["Date"]).dt.year == today.year)
]

# Total spent this month
total_monthly_spent = monthly_expenses["Amount"].sum()
st.markdown(f"### Total Spent - {today.strftime('%B %Y')}: ₹{total_monthly_spent:.2f}")
st.progress(min(total_monthly_spent / 10000, 1.0))  # Change 10000 to your average monthly threshold if needed

# Category-wise breakdown and alerts
st.subheader("Category Breakdown")
breakdown = monthly_expenses.groupby("Type")["Amount"].sum().reset_index()

# Loop through each category
for section in expense_categories:
    spent = breakdown[breakdown["Type"] == section]["Amount"].sum()
    cap = st.session_state.budget_caps.get(section, 0.0)
    remaining_budget = cap - spent
    low_budget_trigger = 0.1 * cap if cap > 0 else 0  # 10% threshold

    # Display usage
    st.markdown(f"*{section}*: ₹{spent:.2f} / ₹{cap:.2f}")
    st.progress(min(spent / cap if cap > 0 else 0, 1.0))

    # Define alert key
    warning_key = f"{today.month}-{today.year}-{section}"

    # Show budget alerts
    if spent > cap:
        st.error(f"Limit exceeded in {section} by ₹{spent - cap:.2f}")
    elif remaining_budget <= low_budget_trigger and remaining_budget > 0:
        if not st.session_state.notified.get(warning_key, False):
            st.warning(f"Alert: Only ₹{remaining_budget:.2f} remaining in your {section} budget.")
            st.session_state.notified[warning_key] = True
    elif spent > 0:
        st.success(f"All good with {section} budget.")

st.divider()

# Display Monthly Expense Table
st.subheader("Detailed Expenses")

# Show expenses sorted by latest date
st.dataframe(
    monthly_expenses.sort_values("Date", ascending=False),
    use_container_width=True
)
