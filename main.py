"""
Personal Finance Tracker CLI application.

Allows users to add transactions, view summaries by month/category, 
visualise summaries by generating charts using pandas and matplotlib.
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np 
from datetime import datetime
import sys
import calendar

class FinanceTracker:
    """
    A personal finance tracker that manages transactions and provides insights.

    Stores income and expenses, and allows filtering, summarising, and 
    visualising spending patterns.
    """

    MONTHS_ABBR = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    MONTHS_FULL = list(calendar.month_name)[1:]
    HEADERS = ["Date", "Category", "Amount", "Description"]
    VALID_CATEGORIES = ["Food", "Entertainment", "Bills", "Leisure", "Transport", "Shopping", "Gifts", "Income", "Refund"]
    INCOME_CATEGORIES = ["Income", "Refund"]
    EXPENSE_CATEGORIES = []
    for c in VALID_CATEGORIES:
        if c not in INCOME_CATEGORIES:
            EXPENSE_CATEGORIES.append(c)
    
    def __init__(self):
        """
        Initialises the DataFrame used to store transactions. 

        Parameters
        ----------
        None
        """

        if Path("transactions.csv").exists():
            df = pd.read_csv("transactions.csv") 
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y") # Converting the dates column from strings to datetime objects to help with filtering transactions
        else:
            df = pd.DataFrame(columns = FinanceTracker.HEADERS)

        self.df = df

    def menu(self):
        """
        Displays the menu to the user.

        Parameters
        ----------
        None

        Raises
        ------
        ValueError 
            If they enter an invalid option or select an option that is not
            within the range of accepted values.

        Returns
        -------
        None
        """

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
                self.add_transaction()
            elif option == 2:
                self.sub_menu()
            elif option == 3:
                self.exit_program()

    def add_transaction(self):
        """
        Add one or more transactions to the tracker. 

        The method prompts the user for details of their transaction, 
        validates their input, appends it to the DataFrame, once the user
        wishes to add no further transactions, transactions are saved to 
        the CSV.

        Parameters
        ----------
        None

        Raises
        ------
        ValueError
            If the date is invalid, category is not recognised,
            amount does not match category type, or description is blank.

            If option to add another transaction is not strictly "Yes" or "No".

        Returns
        -------
        None
        """

        total_transactions = 0

        while True:
            print("")

            total_transactions += 1

            while True:
                try:
                    date = input("Enter the date (DD-MM-YYYY): ")
                    parsed_date = datetime.strptime(date, "%d-%m-%Y") # Ensure the date entered is in the correct format
                except ValueError as e:
                    print(e)
                else:
                    break

            while True:
                try:
                    print(f"\nCategories:\n")
                    print(f"\n".join(FinanceTracker.VALID_CATEGORIES))
                    category = input(f"\nEnter a valid category from the above: ").strip().capitalize()
                    if category not in FinanceTracker.VALID_CATEGORIES:
                        raise ValueError("Not a valid category")
                except ValueError as e:
                    print(e)
                else:
                    break

            while True:
                try:
                    amount = float(input("Enter the amount (positive for income/refund, negative for expenses): "))
                    # Ensure sign matches category: income/refunds must be positive, expenses must be negative
                    if category in FinanceTracker.INCOME_CATEGORIES and amount <= 0:
                        raise ValueError(f"{category} must be positive")
                    elif category not in FinanceTracker.INCOME_CATEGORIES and amount >= 0:
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
            # Append the new transaction (as a 1-row DataFrame) to the existing DataFrame, and reset the index to keep it continuous
            self.df = pd.concat([self.df, pd.DataFrame([transaction])], ignore_index = True) 

            print("")

            while True:
                try:
                    add_another_transaction = input("Would you like to add another transaction (Yes/No)? ").strip().capitalize()
                    if add_another_transaction != "Yes" and add_another_transaction != "No":
                        raise ValueError("Incorrect value entered")
                except ValueError as e:
                    print(e)
                else:
                    break
            
            if add_another_transaction == "Yes":
                pass
            elif add_another_transaction == "No":
                self.save_to_csv()

                print(f"\n{total_transactions} transaction(s) added successfully")
                break

    def sub_menu(self):
        """
        Displays the sub-menu to the user.

        Parameters
        ----------
        None

        Raises
        ------
        ValueError 
            If they enter an invalid option or select an option that is not
            within the range of accepted values.

        Returns
        -------
        None
        """

        while True:
            while True:
                try:
                    option = int(input(f"\n1) View by month \n2) View by category \n3) View cumulative net balance \n4) View all-time overview \n5) Go back \n\nSelect an option: "))
                    if option < 1 or option > 5:
                        raise ValueError("Input must be between 1 and 5")
                except ValueError as e:
                    print(e)
                else:
                    break 

            if option == 1:
                self.view_by_month()

            elif option == 2:
                self.view_by_category()

            elif option == 3:
                self.view_cumulative_net_balance()

            elif option == 4:
                self.view_all_time_overview()

            elif option == 5:
                break
    
    @staticmethod
    def exit_program():
        """
        Helper method to terminate the program safely. 

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        print("Closing program...")
        sys.exit(0)

    def view_by_month(self):
        """
        Displays a financial summary for a given month.

        Prompts the user to enter a month. Calculates the sum for each category
        and calculates total income/expense. 
        
        Optionally displays:
            - Bar chart of expenses by category
            - Horizontal bar chart of income vs expenses
            - Pie chart of expense breakdown

        Parameters
        ----------
        None

        Raises
        ------
        ValueError
            If the month is not a valid month name.

        Returns
        -------
        None
        """

        while True:
            try: 
                month = input(f"\nEnter the full month name: ").strip().capitalize()
                if month not in FinanceTracker.MONTHS_FULL:
                    raise ValueError("Incorrect month name")
            except ValueError as e:
                print(e)
            else:
                break

        print(f"\n----------------------------")

        print(f"\nSummary for {month}:\n")

        # Filter rows for the given month, then group by category and sum the amounts
        summary = self.df[self.df["Date"].dt.month_name() == month].groupby("Category")["Amount"].sum()  

        # Filter rows for the given month and categories in INCOME_CATEGORIES, then sum the amounts
        total_income = self.df[(self.df["Date"].dt.month_name() == month) & (self.df["Category"].isin(FinanceTracker.INCOME_CATEGORIES))]["Amount"].sum() 

        # Filter rows for the given month and categories in EXPENSE_CATEGORIES, then sum the amounts
        total_expenses = self.df[(self.df["Date"].dt.month_name() == month) & (self.df["Category"].isin(FinanceTracker.EXPENSE_CATEGORIES))]["Amount"].sum()

        for category, amount in summary.items(): 
            print(f"{category}: £{amount:.2f}")

        print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

        print(f"\n----------------------------")

        if self.get_visualisation_choice() == "Yes":
            # Drops any categories listed in INCOME_CATEGORIES if they exist, if they don't, no error is raised
            summary_without_income = summary.drop(FinanceTracker.INCOME_CATEGORIES, errors = "ignore") 

            fig = plt.figure(figsize = (8, 5))
            fig.canvas.manager.set_window_title(f"Month: {month}")

            ''' Chart 1 '''
            x1 = np.array(summary_without_income.index)
            y1 = np.array(summary_without_income.values.__abs__()) # Convert expenses to absolute values so bars display as positive amounts

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

    def view_by_category(self):
        """
        Displays a financial summary for a given category.

        Prompts the user to enter a category. Calculates the sum for each month in the year.
        Additionally, it calculates the number of transactions for each month for that category and also 
        calculates the average spent per transaction for each month. 

        Optionally displays:
            - Bar chart of category by month
            - Line chart of average per transaction by month
            - Bar chart of total number of transactions by month

        Parameters
        ----------
        None

        Raises
        ------
        ValueError
            If the category is not a valid category.

        Returns
        -------
        None
        """

        while True:
            try:
                print("\nCategories:\n")
                print("\n".join(FinanceTracker.VALID_CATEGORIES))
                category = input(f"\nEnter a valid category from the above: ").strip().capitalize()
                if category not in FinanceTracker.VALID_CATEGORIES:
                    raise ValueError("Not a valid category")
            except ValueError as e:
                print(e)
            else:
                break

        print(f"\n----------------------------")

        print(f"\nSummary for {category} category:\n")

        # Filter rows for the given category, then group by month and sum the amounts 
        summary = self.df[self.df["Category"] == category].groupby(self.df["Date"].dt.month)["Amount"].sum()
        
        # Count the number of transactions per month for the given category
        number_of_transactions = self.df[self.df["Category"] == category].groupby(self.df["Date"].dt.month)["Amount"].count()
        amount_of_transactions_per_month = []

        for month, amount in summary.items():
            count = number_of_transactions.get(month)
            amount_of_transactions_per_month.append(count)
            print(f"{FinanceTracker.MONTHS_ABBR[month]}: £{amount:.2f} ({count} transaction(s), avg per transaction: £{amount/count:.2f})")

        print(f"\n----------------------------")

        if self.get_visualisation_choice() == "Yes":
            month_names = [FinanceTracker.MONTHS_ABBR[m] for m in summary.index]

            if category == "Income":
                chart1_title = "Monthly Total Income"
                chart2_title = "Average Income per Transaction"
                chart3_title = "Number of Income Transactions"
            elif category == "Refund":
                chart1_title = "Monthly Total Refund"
                chart2_title = "Average Refund per Transaction"
                chart3_title = "Number of Refund Transactions"
            elif category in FinanceTracker.EXPENSE_CATEGORIES:
                chart1_title = "Monthly Total Spend"
                chart2_title = "Average Spend per Transaction"
                chart3_title = "Number of Transactions"

            fig = plt.figure(figsize = (8, 5))
            fig.canvas.manager.set_window_title(f"Category: {category}")

            ''' Chart 1'''
            x1 = np.array(month_names)
            y1 = np.array(summary.values.__abs__()) # Convert the values to absolute values so bars display as positive amounts

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
            plt.plot(x2, y2, marker = "o", mfc = "#2ca02c", c = "#2ca02c", linestyle = "--", linewidth =  1, markersize = 4)

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

    def view_cumulative_net_balance(self):
        """
        Displays the cumulative net balance for the year.

        Calculates the net balance (total income - total expense) for each month
        and then works out the cumulative net balance.

        Optionally displays:
            - Bar chart of net balance by month 
            - Line chart of cumulative net balance by month

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        print(f"\n----------------------------")

        print(f"\nCumulative Net Balance:\n")

        # Filter rows for categories in INCOME_CATEGORIES, then group by month and sum the amounts
        total_income_per_month = self.df[self.df["Category"].isin(FinanceTracker.INCOME_CATEGORIES)].groupby(self.df["Date"].dt.month)["Amount"].sum()

        # Filter rows for categories in EXPENSE_CATEGORIES, then group by month and sum the amounts 
        total_expenses_per_month = self.df[self.df["Category"].isin(FinanceTracker.EXPENSE_CATEGORIES)].groupby(self.df["Date"].dt.month)["Amount"].sum()

        net = total_income_per_month + total_expenses_per_month
        cumulative_net_balance = net.cumsum() # Work out the cumulative net balance over time

        for month, amount in cumulative_net_balance.items():
            print(f"{FinanceTracker.MONTHS_ABBR[month]}: £{amount:.2f}")

        print(f"\n----------------------------")

        if self.get_visualisation_choice() == "Yes":
            month_names = [FinanceTracker.MONTHS_ABBR[m] for m in net.index]

            fig = plt.figure(figsize = (8, 5))
            fig.canvas.manager.set_window_title("Cumulative Net Balance")

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
            plt.plot(x2, y2, marker = "o", mfc = "#00BFFF", c = "#00BFFF", linestyle = "--", linewidth =  1, markersize = 4)

            plt.title("Cumulative Net Balance Over Time")
            plt.xlabel("Months")
            plt.ylabel("Cumulative (£)")

            plt.tight_layout()
            plt.show()

    def view_all_time_overview(self):
        """
        Displays an all-time overview of the balance from start to end of the year.

        Calcualtes the sum for each category and calculates the total income/expenses.

        Optionally displays:
            - Bar chart of expenses by category
            - Horizontal bar chart of income vs expenses

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        print(f"\n----------------------------")

        print(f"\nAll-time Overview by Category:\n")

        # Groups by category and sums the amounts
        summary = self.df.groupby("Category")["Amount"].sum()

        # Filters rows for categories in INCOME_CATEGORIES, then sums the amounts 
        total_income = self.df[self.df["Category"].isin(FinanceTracker.INCOME_CATEGORIES)]["Amount"].sum()

        # Filters rows for categories in EXPENSE_CATEGORIES, then sums the amounts 
        total_expenses = self.df[self.df["Category"].isin(FinanceTracker.EXPENSE_CATEGORIES)]["Amount"].sum()

        for category, amount in summary.items():
            print(f"{category}: £{amount:.2f}")

        print(f"\nTotal income: £{total_income:.2f} \nTotal expenses: £{total_expenses:.2f}")

        print(f"\n----------------------------")

        if self.get_visualisation_choice() == "Yes":
            # Drops any categories listed in INCOME_CATEGORIES if they exist, if they don't, no error is raised
            summary_without_income = summary.drop(FinanceTracker.INCOME_CATEGORIES, errors = "ignore")
            
            fig = plt.figure(figsize = (8, 5))
            fig.canvas.manager.set_window_title("All-time Overview")

            ''' Chart 1 '''
            x1 = np.array(summary_without_income.index)
            y1 = np.array(summary_without_income.values.__abs__()) # Convert expenses to absolute values so bars display as positive amounts

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

    @staticmethod
    def get_visualisation_choice():
        """
        Helper method to ask the user whether they want a visual representation of the data.

        Parameters
        ----------
        None

        Raises
        ------
        ValueError
            If choice is not strictly "Yes" or "No".

        Returns
        -------
        str
            The user's choice ("Yes" or "No").
        """

        while True:
            try:
                choice = input(f"\nWould you like a visual representation of this data (Yes/No)? ").strip().capitalize()
                if choice != "Yes" and choice != "No":
                    raise ValueError("Incorrect value entered")
            except ValueError as e:
                print(e)
            else:
                return choice
            
    def save_to_csv(self):
        """
        Saves the DataFrame to the CSV.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Save the whole DataFrame to CSV in one go
        df_to_save = self.df.copy()
        df_to_save["Date"] = df_to_save["Date"].dt.strftime("%d-%m-%Y") # Format the Date column as DD-MM-YYYY strings
        df_to_save.to_csv("transactions.csv", index = False) 

ft = FinanceTracker()
ft.menu()