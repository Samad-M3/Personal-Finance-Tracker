import csv
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime
import sys

months_abbr = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
valid_categories = ["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts", "Income", "Refund"]
headers = ["Date", "Category", "Amount", "Description"]

if Path("transactions.csv").exists():
    df = pd.read_csv("transactions.csv") # Reading from CSV file  
    date_object = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df["Date"] = date_object # Converting the dates column from strings to datetime objects to help with filtering transactions
else:
    df = pd.DataFrame(columns = headers)

def menu():
    while True:
        while True:
            try:
                option = int(input(f"\n1) Add a transaction \n2) View transaction(s) \n3) Exit \n\nSelect an option: "))
                if option < 1 or option > 3:
                    raise ValueError("Input must be between 1 and 3")
            except ValueError as e:
                print(e)
            else:
                break

        if option == 1:
            add_transaction()
        elif option == 2:
            sub_menu()
        elif option == 3:
            exit_program()

def add_transaction():
    global df
    count = 0

    while True:
        print("")

        count += 1

        while True:
            try:
                date = input("Enter the date (DD-MM-YYYY): ")
                parsed_date = datetime.strptime(date, "%d-%m-%Y")
            except ValueError as e:
                print(e)
            else:
                break

        while True:
            try:
                category = input(f"\nCategories: \n\nFood\nEntertainment\nBills\nLeisure\nTransport\nShopping\nGifts\nIncome\nRefund \n\nEnter a valid category from the above: ").strip().capitalize()
                if category not in valid_categories:
                    raise ValueError("Not a valid category")
            except ValueError as e:
                print(e)
            else:
                break

        while True:
            try:
                amount = float(input("Enter the amount (positive for income/refund, negative for expenses): "))
                income_categories = ["Income", "Refund"]
                if category in income_categories and amount <= 0:
                    raise ValueError(f"{category} must be positive")
                elif category not in income_categories and amount >= 0:
                    raise ValueError(f"{category} must be negative")
            except ValueError as e:
                print(e)
            else:
                break

        while True:
            try:
                description = input("Enter a description: ").strip().capitalize()
                if description == "":
                    raise ValueError("Cannot be left blank")
            except ValueError as e:
                print(e)
            else: 
                break

        transaction = {
            "Date": parsed_date,
            "Category": category,
            "Amount": amount,
            "Description":description
        }
        df = pd.concat([df, pd.DataFrame([transaction])], ignore_index = True)

        print("")

        while True:
            try:
                add_another_transaction = input("Would you like to add another transaction (yes/no)? ").strip().lower()
                if add_another_transaction != "yes" and add_another_transaction != "no":
                    raise ValueError("Incorrect value entered")
            except ValueError as e:
                print(e)
            else:
                break
        
        if add_another_transaction == "yes":
            pass
        elif add_another_transaction == "no":
            # Save the whole df to CSV in one go
            df_to_save = df.copy()
            df_to_save["Date"] = df_to_save["Date"].dt.strftime("%d-%m-%Y")
            df_to_save.to_csv("transactions.csv", index = False)

            print(f"\n{count} transaction(s) added successfully")
            break

def sub_menu():
    while True:
        option = int(input(f"\n1) View by month \n2) View by category \n3) View cumulative net balance \n4) View all-time overview \n5) Go back \n\nSelect an option: ")) 

        if option == 1:
            month = input(f"\nEnter the full month name: ").strip().capitalize()

            print(f"\n----------------------------")

            print(f"\nSummary for {month}:\n")

            summary = df[df["Date"].dt.month_name() == month].groupby("Category")["Amount"].sum()
            summary.index.name = None

            total_income = df[(df["Date"].dt.month_name() == month) & (df["Category"].isin(["Income", "Refund"]))]["Amount"].sum()
            total_expenses = df[(df["Date"].dt.month_name() == month) & (df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"]))]["Amount"].sum()

            for category, amount in summary.items():
                print(f"{category}: £{amount:.2f}")

            print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

            print(f"\n----------------------------")

            visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

            if visualise_transaction.lower() == "yes":
                summary_without_income = summary.drop(["Income", "Refund"], errors = "ignore")

                fig = plt.figure(figsize = (8, 5))
                fig.canvas.manager.set_window_title(f"Month: {month}")

                ''' Chart 1 '''
                x1 = np.array(summary_without_income.index)
                y1 = np.array(summary_without_income.values.__abs__())

                plt.subplot(3, 1, 1)
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

        elif option == 2:
            category = input(f"\nCategories: \n\nFood\nEntertainment\nBills\nLeisure\nTransport\nShopping\nGifts\nIncome\nRefund \n\nEnter a valid category from the above: ").strip().capitalize()

            print(f"\n----------------------------")

            print(f"\nSummary for {category} category:\n")

            summary = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].sum()
            summary.index.name = None
            number_of_transactions = df[df["Category"] == category].groupby(df["Date"].dt.month)["Amount"].count()
            amount_of_transactions_per_month = []

            for month, amount in summary.items():
                count = number_of_transactions.get(month)
                amount_of_transactions_per_month.append(count)
                print(f"{months_abbr[month]}: £{amount:.2f} ({count} transaction(s), avg per transaction: £{amount/count:.2f})")

            print(f"\n----------------------------")

            visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

            if visualise_transaction.lower() == "yes":
                month_names = [months_abbr[m] for m in summary.index]

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

                fig = plt.figure(figsize = (8, 5))
                fig.canvas.manager.set_window_title(f"Category: {category}")

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

        elif option == 3:
            print(f"\n----------------------------")

            print(f"\nCumulative net balance:\n")

            total_income_per_month = df[df["Category"].isin(["Income", "Refund"])].groupby(df["Date"].dt.month)["Amount"].sum()
            total_expenses_per_month = df[df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"])].groupby(df["Date"].dt.month)["Amount"].sum()
            net = total_income_per_month + total_expenses_per_month
            cumulative_net_balance = net.cumsum()
            net.index.name = None

            for month, amount in cumulative_net_balance.items():
                print(f"{months_abbr[month]}: £{amount:.2f}")

            print(f"\n----------------------------")

            visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

            if visualise_transaction.lower() == "yes":
                month_names = [months_abbr[m] for m in net.index]

                fig = plt.figure(figsize = (8, 5))
                fig.canvas.manager.set_window_title(f"Cumulative Net Balance")

                ''' Chart 1 '''
                x1 = np.array(month_names)
                y1 = np.array(net.values)

                plt.subplot(2, 1, 1)
                plt.grid(alpha = 0.3, linestyle = '--')
                plt.bar(x1, y1)

                plt.title("Monthly Net Balance (Income - Expenses)")
                plt.xlabel("Months")
                plt.ylabel("Net (£)")

                ''' Chart 2 '''
                x2 = np.array(month_names)
                y2 = np.array(cumulative_net_balance.values)

                plt.subplot(2, 1, 2)
                plt.grid(alpha = 0.3, linestyle = '--')
                plt.plot(x2, y2, marker = "o", mfc = "#00BFFF", c = "#00BFFF", linestyle = "--", linewidth =  1, ms = 4)

                plt.title("Cumulative Net Balance Over Time")
                plt.xlabel("Months")
                plt.ylabel("Cumulative (£)")

                plt.tight_layout()
                plt.show()

        elif option == 4:
            print(f"\n----------------------------")

            print(f"\nAll-time overview per category:\n")

            summary = df.groupby("Category")["Amount"].sum()
            summary.index.name = None

            total_income = df[df["Category"].isin(["Income", "Refund"])]["Amount"].sum()
            total_expenses = df[df["Category"].isin(["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts"])]["Amount"].sum()

            for category, amount in summary.items():
                print(f"{category}: £{amount:.2f}")

            print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

            print(f"\n----------------------------")

            visualise_transaction = input(f"\nWould you like a visual representation of this data? ")

            if visualise_transaction.lower() == "yes":
                summary_without_income = summary.drop(["Income", "Refund"], errors = "ignore")
                
                fig = plt.figure(figsize = (8, 5))
                fig.canvas.manager.set_window_title(f"All-time Overview")

                ''' Chart 1 '''
                x1 = np.array(summary_without_income.index)
                y1 = np.array(summary_without_income.values.__abs__())

                plt.subplot(2, 1, 1)
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
                plt.grid(alpha = 0.3, linestyle = '--')
                plt.barh(x2, y2, color = colours, height = 0.6)

                plt.title("Total Income VS Total Expenses")
                plt.xlabel("Amount (£)")

                plt.tight_layout()
                plt.show()

        elif option == 5:
            break
   
def exit_program():
    print("Closing program...")
    sys.exit(0)

menu()