transactions = []

add_transaction = True

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

    another_transaction = input("Would you like to add another transaction? ")
    
    if another_transaction.lower() == "yes":
        pass
    elif another_transaction.lower() == "no":
        print(f"\nAll transactions added successfully")
        add_transaction = False

for t in transactions:
    print(f"\nDate: {t['Date']} \nCategory: {t['Category']} \nAmount: {t['Amount']} \nDescription: {t['Description']}") 