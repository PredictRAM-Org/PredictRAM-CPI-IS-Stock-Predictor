import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from pandas import json_normalize

# Function to load data from stock data folder
def load_data():
    # Replace 'path/to/stock_data/folder' with the actual path to your stock data folder
    folder_path = 'stock_data'

    # Load balance sheet and income statement data
    with open(f'{folder_path}/balance_sheet.json') as f:
        balance_sheet_data = json.load(f)

    with open(f'{folder_path}/income_statement.json') as f:
        income_statement_data = json.load(f)

    # Convert JSON data to Pandas DataFrame
    balance_sheet = json_normalize(balance_sheet_data)
    income_statement = json_normalize(income_statement_data)

    return balance_sheet, income_statement

# Function to display tables
def display_tables(balance_sheet, income_statement):
    st.subheader('Balance Sheet')
    st.dataframe(balance_sheet)

    st.subheader('Income Statement')
    st.dataframe(income_statement)

# Function to generate and display a chart
def generate_chart(balance_sheet, income_statement):
    # Replace 'column_name' with the column you want to use for the chart
    column_name = 'example_column'

    # Plotting a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(balance_sheet['Date'], balance_sheet[column_name], label='Balance Sheet')
    plt.bar(income_statement['Date'], income_statement[column_name], label='Income Statement')

    plt.xlabel('Date')
    plt.ylabel(column_name)
    plt.title(f'Balance Sheet and Income Statement: {column_name}')
    plt.legend()

    st.subheader('Chart')
    st.pyplot()

def main():
    st.title('Stock Data Analysis App')

    # Load data
    balance_sheet, income_statement = load_data()

    # Display tables
    display_tables(balance_sheet, income_statement)

    # Generate and display chart
    generate_chart(balance_sheet, income_statement)

if __name__ == '__main__':
    main()
