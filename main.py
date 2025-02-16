import os

FILE_NAME = "products.txt"
BILL_FILE = "bill_receipt.txt"


def add_product():
    product_name = input("Enter Product Name: ").strip()
    if not product_name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter Price: ").strip())
        total_stock = int(input("Enter Total Stock: ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric values for price and stock.")
        return

    with open(FILE_NAME, "a") as file:
        file.write(f"{product_name}, {price}, {total_stock}\n")
    print("Product added successfully!")


def display_products():
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        print("No products available.")
        return
    print("\nProduct Records:")
    with open(FILE_NAME, "r") as file:
        for line in file:
            try:
                product_name, price, total_stock = line.strip().split(", ")
                print(f"Product: {product_name}, Price: ${price}, Stock: {total_stock}")
            except ValueError:
                print(f"Malformed line skipped: {line.strip()}")


def search_product():
    product_name = input("Enter Product Name to search: ").strip()

    with open(FILE_NAME, "r") as file:
        for line in file:
            record = line.strip().split(", ")
            if record[0].lower() == product_name.lower():
                print(f"Found: {record[0]}, Price: ${record[1]}, Stock: {record[2]}")
                return
    print("Product not found.")


def edit_product():
    product_name = input("Enter Product Name to edit: ").strip()
    updated_records = []
    found = False

    with open(FILE_NAME, "r") as file:
        for line in file:
            record = line.strip().split(", ")
            if record[0].lower() == product_name.lower():
                found = True
                new_price = input(f"New Price (current: {record[1]}): ") or record[1]
                new_stock = input(f"New Stock (current: {record[2]}): ") or record[2]
                updated_records.append(f"{product_name}, {new_price}, {new_stock}\n")
            else:
                updated_records.append(line)

    if found:
        with open(FILE_NAME, "w") as file:
            file.writelines(updated_records)
        print("Product updated successfully!")
    else:
        print("Product not found.")


def delete_product():
    product_name = input("Enter Product Name to delete: ").strip()
    updated_records = []
    found = False

    with open(FILE_NAME, "r") as file:
        for line in file:
            record = line.strip().split(", ")
            if record[0].lower() == product_name.lower():
                found = True
                print(f"Product '{product_name}' deleted.")
            else:
                updated_records.append(line)

    if found:
        with open(FILE_NAME, "w") as file:
            file.writelines(updated_records)
    else:
        print("Product not found.")


def generate_bill():
    cart = {}
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        print("No products available to generate a bill.")
        return

    while True:
        display_products()
        choice = input("Enter product name to add to bill (or 'done' to finish): ").strip()
        if choice.lower() == "done":
            break
        with open(FILE_NAME, "r") as file:
            for line in file:
                record = line.strip().split(", ")
                if record[0].lower() == choice.lower():
                    try:
                        quantity = int(input(f"Enter quantity for {choice}: ").strip())
                        stock = int(record[2])
                        if stock == 0:
                            print("Sorry, stock out.")
                        elif quantity > stock:
                            print("Not enough stock available.")
                        else:
                            total_price = float(record[1]) * quantity
                            cart[choice] = total_price
                    except ValueError:
                        print("Invalid quantity. Please enter a number.")
                    break
            else:
                print("Product not found.")

    if cart:
        total = sum(cart.values())
        with open(BILL_FILE, "w") as file:
            file.write("\n--- Bill Receipt ---\n")
            for item, price in cart.items():
                file.write(f"{item}: ${price}\n")
            file.write(f"\nTotal Amount: ${total}\n")
        print("Bill generated successfully!\n")
        for item, price in cart.items():
            print(f"{item}: ${price}")
        print(f"Total: ${total}")
    else:
        print("No items in the bill.")


def main_menu():
    while True:
        print("\n Inventory & Billing System:")
        print("1. Add Product")
        print("2. Display All Products")
        print("3. Search Product")
        print("4. Edit Product")
        print("5. Delete Product")
        print("6. Generate Bill")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_product()
        elif choice == "2":
            display_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            edit_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            generate_bill()
        elif choice == "7":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
