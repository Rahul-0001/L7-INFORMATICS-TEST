import streamlit as st
import pandas as pd
from datetime import datetime

# Page Setup
st.set_page_config(page_title="Budget Buddy", layout="centered")

st.title("Budget Buddy: Expense and Savings Tracker")
st.markdown("Track your expenses and manage your monthly budget effectively.")

# Initialize state variables
if 'expense_data' not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(columns=["Date", "Type", "Amount", "Details"])

if 'budget_caps' not in st.session_state:
    st.session_state.budget_caps = {}

if 'notified' not in st.session_state:
    st.session_state.notified = {}

st.divider()

# --- Expense Entry ---
st.header("Log Expense")
with st.form("log_form"):
    col_left, col_right = st.columns(2)
    with col_left:
        input_date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment"])
    with col_right:
        value = st.number_input("Amount in ₹", min_value=0.0, step=0.01, format="%.2f")
        description = st.text_input("Short Note (optional)")
    save = st.form_submit_button("Save Entry")

    if save:
        new_row = pd.DataFrame([[input_date, category, value, description]], columns=st.session_state.expense_data.columns)
        st.session_state.expense_data = pd.concat([st.session_state.expense_data, new_row], ignore_index=True)
        st.success("Entry recorded successfully.")

st.divider()

# --- Budget Configuration ---
st.header("Set Monthly Budget")
expense_categories = ["Food", "Transport", "Entertainment"]
budget_inputs = st.columns(len(expense_categories))
for idx, group in enumerate(expense_categories):
    with budget_inputs[idx]:
        st.session_state.budget_caps[group] = st.number_input(
            f"{group} Budget", min_value=0.0, value=st.session_state.budget_caps.get(group, 0.0), key=f"cap_{group}"
        )

st.divider()

# --- Monthly Insights ---
st.header("Current Month Overview")

today = datetime.today()
monthly_expenses = st.session_state.expense_data[
    (pd.to_datetime(st.session_state.expense_data["Date"]).dt.month == today.month) &
    (pd.to_datetime(st.session_state.expense_data["Date"]).dt.year == today.year)
]

total_monthly_spent = monthly_expenses["Amount"].sum()
st.markdown(f"### Total Spent - {today.strftime('%B %Y')}: ₹{total_monthly_spent:.2f}")
st.progress(min(total_monthly_spent / 10000, 1.0))  # You can customize the limit

# Per-Category Report
st.subheader("Category Breakdown")
breakdown = monthly_expenses.groupby("Type")["Amount"].sum().reset_index()

for section in expense_categories:
    spent = breakdown[breakdown["Type"] == section]["Amount"].sum()
    cap = st.session_state.budget_caps.get(section, 0.0)
    remaining_budget = cap - spent
    low_budget_trigger = 0.1 * cap if cap > 0 else 0

    st.markdown(f"*{section}*: ₹{spent:.2f} / ₹{cap:.2f}")
    st.progress(min(spent / cap if cap > 0 else 0, 1.0))

    warning_key = f"{today.month}-{today.year}-{section}"
    if spent > cap:
        st.error(f"Limit exceeded in {section} by ₹{spent - cap:.2f}")
    elif remaining_budget <= low_budget_trigger and remaining_budget > 0:
        if not st.session_state.notified.get(warning_key, False):
            st.warning(f"Alert: Only ₹{remaining_budget:.2f} remaining in your {section} budget.")
            st.session_state.notified[warning_key] = True
    elif spent > 0:
        st.success(f"All good with {section} budget.")

st.divider()

# --- Expense Table ---
st.subheader("Detailed Expenses")
st.dataframe(monthly_expenses.sort_values("Date", ascending=False), use_container_width=True)