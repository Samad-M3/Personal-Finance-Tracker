import csv
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
import sys

transactions = []
calendar = {1: "January", 2: "February", 3: "March", 4: "Arpil", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

def menu():
    print(f"\n1) Add a transaction \n2) View transaction(s) \n3) Exit")
    option = int(input(f"\nSelect an option: "))

    if option == 1:
        add_transaction()
    elif option == 2:
        sub_menu()
    elif option == 3:
        exit()

def add_transaction():
    add_transaction_bool = True
    count = 0

    while add_transaction_bool:
        print("")

        count += 1

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

        add_another_transaction = input("Would you like to add another transaction (yes/no)? ")
        
        if add_another_transaction.lower() == "yes":
            pass
        elif add_another_transaction.lower() == "no":
            file_exists = Path("transactions.csv").exists()
            headers = ["Date", "Category", "Amount", "Description"]

            if not file_exists:
                with open("transactions.csv", "w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()

            with open("transactions.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerows(transactions)

            print(f"\n{count} transaction(s) added successfully")

            menu()
            # add_transaction_bool = False

def sub_menu():
    df = pd.read_csv("transactions.csv") # Reading from CSV file    
    date_object = pd.to_datetime(df["Date"], format="%d-%m-%Y") # Converting the dates column from strings to datetime objects 
    df["Date"] = date_object

    print(f"\n1) View by month \n2) View by category \n3) View all-time spending by category \n4) Go back")
    option = int(input(f"\nSelect an option: ")) 

    if option == 1:
        month = input("Enter the full month name: ").strip().title()
        print(f"\nSummary for {month}:\n")

        summary = df[df["Date"].dt.month_name() == month].groupby("Category")["Amount"].sum()
        summary.index.name = None
        total_income = df[(df["Date"].dt.month_name() == month) & (df["Category"].isin(["Income", "Refund"]))]["Amount"].sum()
        total_expenses = df[(df["Date"].dt.month_name() == month) & (df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"]))]["Amount"].sum()

        for category, amount in summary.items():
            print(f"{category}: £{amount:.2f}")

        print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

        sub_menu()
    elif option == 2:
        category = input(f"\nCategories: \n\nFood\nEntertainment\nBills\nLeisure\nTransport\nShopping\nGifts\nIncome\nRefund \n\nEnter a valid category from above: ").strip().title()
        print(f"\nSummary for {category} category:\n")

        summary = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].sum()
        summary.index.name = None
        number_of_transactions = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].count()

        for month, amount in summary.items():
            count = number_of_transactions.get(month)
            print(f"{calendar[month]}: £{amount:.2f} ({count} transaction(s), avg per transaction: £{amount/count:.2f})")
        
        sub_menu()
    elif option == 3:
        print(f"\nAll-time spending per category:\n")

        summary = df.groupby("Category")["Amount"].sum()
        summary.index.name = None

        for category, amount in summary.items():
            print(f"{category}: £{amount:.2f}")
        
        sub_menu()
    elif option == 4:
        menu()
   
def exit_program():
    print("Closing program...")
    sys.exit(0)

menu()

# file_exists = Path("transactions.csv").exists()
# headers = ["Date", "Category", "Amount", "Description"]

# if not file_exists:
#     with open("transactions.csv", "w", newline="") as f:
#         writer = csv.DictWriter(f, fieldnames=headers)
#         writer.writeheader()

# with open("transactions.csv", "a", newline="") as f:
#     writer = csv.DictWriter(f, fieldnames=headers)
#     writer.writerows(transactions)

# df = pd.read_csv("transactions.csv") # Reading from CSV file    

# date_object = pd.to_datetime(df["Date"], format="%d-%m-%Y") # Converting the dates column from strings to datetime objects 
# df["Date"] = date_object

""" Hard-coded filtering """

''' Filter by Category '''

# print(df[df["Category"] == "Food"]) 
# print(df[df["Category"] == "Entertainment"])
# print(df[df["Category"] == "Transport"])

''' Filter by Month '''

# print(df[df["Date"].dt.month == 9])
# print(df[df["Date"].dt.month == 10])
# print(df[df["Date"].dt.month == 12])

''' Combined Filters '''

# print(df[(df["Category"] == "Food") & (df["Date"].dt.month == 11)])
# print(df[(df["Category"] == "Entertainment") & (df["Date"].dt.month == 8)])

''' Aggregation '''

# print(df[df["Date"].dt.month == 10].groupby("Category")["Amount"].sum()) # Total spending per category in October
# print(df.groupby(df["Date"].dt.month_name())["Amount"].sum()) # Total spending for each month
# print(df["Amount"].max()) # Largest single transaction
