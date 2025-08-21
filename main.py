import csv
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

transactions = []

add_transaction = True

start_adding_transactions = input("Would you like to start entering transactions (yes/no): ")

if start_adding_transactions.lower() == "yes":
    while add_transaction:
        print("")

        date = input("Enter the date (DD-MM-YYYY): ")
        category = input("Enter the category: ")
        amount = float(input("Enter the amount (positive for income, negative for expenses): "))
        description = input("Enter a description: ")

        transaction = {
            "Date": date,
            "Category": category,
            "Amount": amount,
            "Description":description
        }

        transactions.append(transaction)

        print("")

        another_transaction = input("Would you like to add another transaction (yes/no)? ")
        
        if another_transaction.lower() == "yes":
            pass
        elif another_transaction.lower() == "no":
            print(f"\nAll transactions added successfully")
            add_transaction = False
elif start_adding_transactions.lower() == "no":
    pass

# for t in transactions:
#     print(f"\nDate: {t['Date']} \nCategory: {t['Category']} \nAmount: {t['Amount']} \nDescription: {t['Description']}") 

file_exists = Path("transactions.csv").exists()
headers = ["Date", "Category", "Amount", "Description"]

if not file_exists:
    with open("transactions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

with open("transactions.csv", "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writerows(transactions)

df = pd.read_csv("transactions.csv")
# print(df.to_string())

""" Hard-coded filtering """

''' Filter by Category '''

# print(df[df["Category"] == "Food"]) 
# print(df[df["Category"] == "Entertainment"])
# print(df[df["Category"] == "Transport"])

''' Filter by Month '''

# print(df[df["Date"].str.contains("-09-")]) 
# print(df[df["Date"].str.contains("-10-")])
# print(df[df["Date"].str.contains("-12-")])

''' Combined Filters '''

# print(df[(df["Category"] == "Food") & (df["Date"].str.contains("-11-"))])
# print(df[(df["Category"] == "Entertainment") & (df["Date"].str.contains("-08-"))])

''' Aggregation '''

# print(df[df["Date"].str.contains("-10-")].groupby("Category")["Amount"].sum()) # Total spending per category in October
