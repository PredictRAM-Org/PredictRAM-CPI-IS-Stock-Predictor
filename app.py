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
        balance_sheet = json_normalize(balance_sheet_data).set_index('Date').T
        income_statement = json_normalize(income_statement_data).set_index('Date').T

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

# Function to generate and display a chart
def generate_chart(balance_sheet, income_statement, stock_name):
    # Replace 'column_name' with the column you want to use for the chart
    column_name = 'Total Assets'

    # Check if the specified column exists in the DataFrame
    if column_name not in balance_sheet.index:
        st.warning(f"Column '{column_name}' not found in the data.")
        return

    # Plotting a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(balance_sheet.index, balance_sheet.loc[column_name], label='Balance Sheet - Total Assets')
    
    # Check if the specified column exists in the income statement DataFrame
    if column_name in income_statement.index:
        plt.bar(income_statement.index, income_statement.loc[column_name], label='Income Statement - Total Revenue')

    plt.xlabel('Date')
    plt.ylabel(column_name)
    plt.title(f'{stock_name} - Balance Sheet and Income Statement: {column_name}')
    plt.legend()

    st.subheader(f'{stock_name} - Chart')
    st.pyplot()

def main():
    st.title('Stock Data Analysis App')

    # Replace 'path/to/stock_data/folder' with the actual path to your stock data folder
    folder_path = 'stock_data'

    # Get the list of stock files in the folder
    stock_files = [file.split('.')[0] for file in os.listdir(folder_path) if file.endswith('.json')]

    # Allow the user to select a stock
    selected_stock = st.selectbox('Select a stock', stock_files)

    # Load data for the selected stock
    balance_sheet, income_statement = load_data(selected_stock, folder_path)

    if balance_sheet is not None and income_statement is not None:
        # Display tables
        display_tables(balance_sheet, income_statement, selected_stock)

        # Generate and display chart
        generate_chart(balance_sheet, income_statement, selected_stock)

if __name__ == '__main__':
    main()
