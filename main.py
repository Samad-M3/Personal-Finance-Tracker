import csv
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np 
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
        exit_program()

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
    date_object = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Date"] = date_object # Converting the dates column from strings to datetime objects to help with filtering transactions

    print(f"\n1) View by month \n2) View by category \n3) View cumulative net balance \n4) View all-time overview \n5) Go back")
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

        visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

        if visualise_transaction.lower() == "yes":
            summary_without_income = summary.drop(["Income", "Refund"], errors = "ignore")

            ''' Chart 1 '''
            x1 = np.array(summary_without_income.index)
            y1 = np.array(summary_without_income.values.__abs__())

            plt.subplot(3, 1, 1)
            # plt.grid(axis = 'y', alpha = 0.3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.bar(x1, y1, width = 0.6)
            
            plt.title("Expenses per Category")
            plt.xlabel("Categories")
            plt.ylabel("Amount (£)")

            ''' Chart 2 '''
            x2 = np.array(["Total Income", "Total Expenses"])
            y2 = np.array([total_income, total_expenses * -1])
            colours = ["#2ECC71", "#E74C3C"]

            plt.subplot(3, 1, 2)
            # plt.grid(axis = 'x', alpha = 0.3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.barh(x2, y2, color = colours)

            plt.title("Total Income VS Total Expenses")
            plt.xlabel("Amount (£)")

            ''' Chart 3 '''
            pie_chart_labels = x1
            y3 = y1

            plt.subplot(3, 1, 3)
            plt.pie(y3, labels = pie_chart_labels)
            plt.title("Expenses Breakdown")

            plt.tight_layout()
            plt.show()

        sub_menu()

    elif option == 2:
        category = input(f"\nCategories: \n\nFood\nEntertainment\nBills\nLeisure\nTransport\nShopping\nGifts\nIncome\nRefund \n\nEnter a valid category from above: ").strip().title()
        print(f"\nSummary for {category} category:\n")

        summary = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].sum()
        summary.index.name = None
        number_of_transactions = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].count()
        amount_of_transactions_per_month = []

        for month, amount in summary.items():
            count = number_of_transactions.get(month)
            amount_of_transactions_per_month.append(count)
            print(f"{calendar[month]}: £{amount:.2f} ({count} transaction(s), avg per transaction: £{amount/count:.2f})")

        visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

        if visualise_transaction.lower() == "yes":
            month_names = [calendar[m] for m in summary.index]

            if category.lower() == "income":
                chart1_title = "Monthly Total Income"
                chart2_title = "Average Income per Transaction"
                chart3_title = "Number of Income Transactions"
            elif category.lower() == "refund":
                chart1_title = "Monthly Total Refund"
                chart2_title = "Average Refund per Transaction"
                chart3_title = "Number of Refund Transactions"
            elif category.lower() in ["food", "entertainment", "bills", "leisure", "transport", "shopping", "gifts"]:
                chart1_title = "Monthly Total Spend"
                chart2_title = "Average Spend per Transaction"
                chart3_title = "Number of Transactions"

            ''' Chart 1'''
            x1 = np.array(month_names)
            y1 = np.array(summary.values.__abs__())

            plt.subplot(3, 1, 1)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.bar(x1, y1)

            plt.title(chart1_title)
            plt.xlabel("Months")
            plt.ylabel("Amount (£)")

            ''' Chart 2 '''  
            x2 = np.array(month_names)
            y2 = np.array(summary.values.__abs__() / amount_of_transactions_per_month)

            plt.subplot(3, 1, 2)
            # plt.grid(alpha = 0.3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.plot(x2, y2, marker = "o", mfc = "#2ca02c", c = "#2ca02c", ls = "--", linewidth =  1, ms = 4)

            plt.title(chart2_title)
            plt.xlabel("Months")
            plt.ylabel("Amount (£)")

            ''' Chart 3 '''
            x3 = np.array(month_names)
            y3 = np.array(amount_of_transactions_per_month)

            plt.subplot(3, 1, 3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.bar(x3, y3, color = "#ff7f0e")

            plt.title(chart3_title)
            plt.xlabel("Months")
            plt.ylabel("Count")

            plt.tight_layout()
            plt.show()

        sub_menu()

    elif option == 3:
        print(f"\nCumulative net balance:\n")

        total_income_per_month = df[df["Category"].isin(["Income", "Refund"])].groupby(df["Date"].dt.month)["Amount"].sum()
        total_expenses_per_month = df[df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"])].groupby(df["Date"].dt.month)["Amount"].sum()
        net = total_income_per_month + total_expenses_per_month
        cumulative_net_balance = net.cumsum()
        net.index.name = None

        for month, amount in cumulative_net_balance.items():
            print(f"{calendar[month]}: £{amount:.2f}")

        visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

        if visualise_transaction.lower() == "yes":
            month_names = [calendar[m] for m in net.index]

            ''' Chart 1 '''
            x1 = np.array(month_names)
            y1 = np.array(net.values)

            plt.subplot(2, 1, 1)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.bar(x1, y1)

            plt.axhline(y = 0, color = 'k', linestyle = '-', linewidth = 1)

            plt.title("Monthly Net Balance (Income - Expenses)")
            plt.xlabel("Months")
            plt.ylabel("Net (£)")

            ''' Chart 2 '''
            x2 = np.array(month_names)
            y2 = np.array(cumulative_net_balance.values)

            plt.subplot(2, 1, 2)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.plot(x2, y2, marker = "o", mfc = "#00BFFF", c = "#00BFFF", linestyle = "--", linewidth =  1, ms = 4)

            plt.axhline(y = 0, color = 'k', linestyle = '-', linewidth = 1)

            plt.title("Cumulative Net Balance Over Time")
            plt.xlabel("Months")
            plt.ylabel("Cumulative (£)")

            plt.tight_layout()
            plt.show()

        sub_menu()

    elif option == 4:
        print(f"\nAll-time overview per category:\n")

        summary = df.groupby("Category")["Amount"].sum()
        summary.index.name = None

        total_income = df[df["Category"].isin(["Income", "Refund"])]["Amount"].sum()
        total_expenses = df[df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"])]["Amount"].sum()

        for category, amount in summary.items():
            print(f"{category}: £{amount:.2f}")

        print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

        visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

        if visualise_transaction.lower() == "yes":
            summary_without_income = summary.drop(["Income", "Refund"], errors = "ignore")
            
            ''' Chart 1 '''
            x1 = np.array(summary_without_income.index)
            y1 = np.array(summary_without_income.values.__abs__())

            plt.subplot(2, 1, 1)
            # plt.grid(axis='y', alpha = 0.3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.bar(x1, y1, width = 0.6)
            
            plt.title("Expenses per Category")
            plt.xlabel("Categories")
            plt.ylabel("Amount (£)")

            ''' Chart 2 '''
            x2 = np.array(["Total Income", "Total Expenses"])
            y2 = np.array([total_income, total_expenses * -1])
            colours = ["#2ECC71", "#E74C3C"]

            plt.subplot(2, 1, 2)
            # plt.grid(axis = 'x', alpha = 0.3)
            plt.grid(alpha = 0.3, linestyle = '--')
            plt.barh(x2, y2, color = colours, height = 0.6)

            plt.title("Total Income VS Total Expenses")
            plt.xlabel("Amount (£)")

            plt.tight_layout()
            plt.show()
        
        sub_menu()

    elif option == 5:
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
