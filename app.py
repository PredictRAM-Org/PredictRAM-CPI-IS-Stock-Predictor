import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from pandas import json_normalize
import os

# Function to load data for a specific stock
def load_data(stock_name, folder_path):
    file_path = os.path.join(folder_path, f'{stock_name}.json')

    if os.path.exists(file_path):
        with open(file_path) as f:
            stock_data = json.load(f)

        # Extracting balance sheet and income statement data
        balance_sheet_data = stock_data.get('BalanceSheet', [])
        income_statement_data = stock_data.get('IncomeStatement', [])

        # Convert JSON data to Pandas DataFrame
        balance_sheet = json_normalize(balance_sheet_data)
        income_statement = json_normalize(income_statement_data)

        # Function to parse mixed-format dates
        def parse_date(date_str):
            try:
                return pd.to_datetime(date_str)
            except pd.errors.OutOfBoundsDatetime:
                # If the above fails, parse the date with a custom format
                return pd.to_datetime(date_str, format='%b-%y')

        # Apply the custom date parsing function to the 'Date' column
        balance_sheet['Date'] = balance_sheet['Date'].apply(parse_date)
        income_statement['Date'] = income_statement['Date'].apply(parse_date)

        # Set Date as the index and sort in descending order
        balance_sheet.set_index('Date', inplace=True)
        balance_sheet.sort_index(ascending=False, inplace=True)
        
        income_statement.set_index('Date', inplace=True)
        income_statement.sort_index(ascending=False, inplace=True)

        return balance_sheet, income_statement
    else:
        st.warning(f"Data not found for stock: {stock_name}")
        return None, None

# Function to display tables
def display_tables(balance_sheet, income_statement, stock_name):
    st.subheader(f'{stock_name} - Balance Sheet')
    st.dataframe(balance_sheet)

    st.subheader(f'{stock_name} - Income Statement')
    st.dataframe(income_statement)

# Function to generate and display a chart for a specific date range
def generate_chart(balance_sheet, income_statement, stock_name, start_date, end_date):
    # Ensure that the indices are sorted before plotting
    balance_sheet_sorted = balance_sheet.sort_index()
    income_statement_sorted = income_statement.sort_index()

    # Filter data for the specified date range
    income_statement_filtered = income_statement_sorted.loc[start_date:end_date]

    # Plotting a line chart for selected columns
    plt.figure(figsize=(10, 6))

    # Plot Total Revenue/Income if available in the income statement DataFrame
    if 'Total Revenue/Income' in income_statement_filtered.columns:
        plt.plot(income_statement_filtered.index, income_statement_filtered['Total Revenue/Income'], label='Total Revenue/Income')

    # Plot Total Operating Expense if available in the income statement DataFrame
    if 'Total Operating Expense' in income_statement_filtered.columns:
        plt.plot(income_statement_filtered.index, income_statement_filtered['Total Operating Expense'], label='Total Operating Expense')

    # Plot Net Income if available in the income statement DataFrame
    if 'Net Income' in income_statement_filtered.columns:
        plt.plot(income_statement_filtered.index, income_statement_filtered['Net Income'], label='Net Income')

    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title(f'{stock_name} - Income Statement Analysis ({start_date} to {end_date})')
    plt.legend()

    st.subheader(f'{stock_name} - Chart')
    st.pyplot()

def main():
    st.title('Stock Data Analysis App')

    # Replace 'path/to/stock_data/folder' with the actual path to your stock data folder
    folder_path = 'path/to/stock_data/folder'

    # Get the list of stock files in the folder
    stock_files = [file.split('.')[0] for file in os.listdir(folder_path) if file.endswith('.json')]

    # Allow the user to select a stock
    selected_stock = st.selectbox('Select a stock', stock_files)

    # Load data for the selected stock
    balance_sheet, income_statement = load_data(selected_stock, folder_path)

    if balance_sheet is not None and income_statement is not None:
        # Display tables with oldest data in first row
        display_tables(balance_sheet, income_statement, selected_stock)

        # Allow the user to specify the date range
        start_date = st.date_input('Select start date', balance_sheet.index[-1])
        end_date = st.date_input('Select end date', balance_sheet.index[0])

        # Generate and display chart for the specified date range
        generate_chart(balance_sheet, income_statement, selected_stock, start_date, end_date)

if __name__ == '__main__':
    main()
