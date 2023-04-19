from transaction import Transaction


def print_menu():
    print("0.Exit")
    print("1.Display categories")
    print("2.Add category")
    print("3.Modify category")
    print("4.Display transactions")
    print("5.Add transaction")
    print("6.Delete transaction")
    print("7.Summarize transactions by date")
    print("8.Summarize transactions by month")
    print("9.Summarize transactions by year")
    print("10.Summarize transactions by category")
    print("11.Print this menu")


def main():
    db_file = "tracker.db"
    transaction = Transaction(db_file)
    print_menu()
    while True:
        choice = input("Please enter an option:")
        if choice == "0":
            break
        elif choice == "1":
            categories = transaction.aggregate_by_category()
            for category in categories:
                print(category[0], category[1])
        elif choice == "2":
            category = input("Please enter a category:")
            transaction.create_transaction("", 0, category, "", "")
        elif choice == "3":
            transaction_id = input("Please enter the transaction ID you want to modify:")
            transaction_data = transaction.read_transaction(transaction_id)
            if transaction_data:
                item = input("Please enter the item name (leave blank if not modifying):")
                amount = input("Please enter the amount (leave blank if not modifying):")
                category = input("Please enter the category (leave blank if not modifying):")
                date = input("Please enter the date (leave blank if not modifying):")
                description = input("Please enter the description (leave blank if not modifying):")
                transaction.update_transaction(transaction_id, item, amount, category, date, description)
            else:
                print("Transaction ID does not exist")
        elif choice == "4":
            # transactions = transaction.cur.execute("SELECT * FROM transactions").fetchall()
            transactions = transaction.read_all_transactions()
            for trans in transactions:
                print(trans)
        elif choice == "5":
            item = input("Please enter the item name:")
            amount = input("Please enter the amount:")
            category = input("Please enter the category:")
            date = input("Please enter the date:")
            description = input("Please enter the description:")
            transaction.create_transaction(item, amount, category, date, description)
        elif choice == "6":
            transaction_id = input("Please enter the transaction ID you want to delete:")
            transaction_data = transaction.read_transaction(transaction_id)
            if transaction_data:
                transaction.delete_transaction(transaction_id)
            else:
                print("Transaction ID does not exist")
        elif choice == "7":
            transactions = transaction.aggregate_by_date()
            for trans in transactions:
                print(trans[0], trans[1])
        elif choice == "8":
            transactions = transaction.aggregate_by_month()
            print(transactions)
            for trans in transactions:
                print(trans[0], trans[1])
        elif choice == "9":
            transactions = transaction.aggregate_by_year()
            for trans in transactions:
                print(trans[0], trans[1])
        elif choice == "10":
            categories = transaction.aggregate_by_category()
            for category in categories:
                print(category[0], category[1])
        elif choice == "11":
            print_menu()
        else:
            print("Invalid option, please try again")

    transaction.close()


if __name__ == "__main__":
    main()
