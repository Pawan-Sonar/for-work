products = []

while True:
    print("\n======================================")
    print("       INVENTORY MANAGEMENT SYSTEM")
    print("======================================")
    print("1. Add Product")
    print("2. View Products")
    print("3. Stock In")
    print("4. Stock Out")
    print("5. Search Product")
    print("6. Low Stock Alert")
    print("7. Calculate Sale")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        product_name = input("Enter product name: ")
        price = int(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))

        product = {
            "name": product_name,
            "price": price,
            "quantity": quantity
        }

        products.append(product)
        print("\nProduct added successfully!")

    elif choice == 2:
        print("\n========== PRODUCTS ==========")

        if len(products) == 0:
            print("No products available.")
        else:
            for product in products:
                print("Name     :", product["name"])
                print("Price    : ₹", product["price"])
                print("Quantity :", product["quantity"])
                print("------------------------------")

    elif choice == 3:
        product_name = input("Enter product name: ")
        stock = int(input("Enter quantity to add: "))
        found = False

        for product in products:
            if product["name"] == product_name:
                product["quantity"] = product["quantity"] + stock
                found = True
                print("\nStock updated successfully!")
                print("New quantity:", product["quantity"])

        if found == False:
            print("Product not found!")

    elif choice == 4:
        product_name = input("Enter product name: ")
        stock = int(input("Enter quantity to remove: "))
        found = False

        for product in products:
            if product["name"] == product_name:
                found = True

                if stock <= product["quantity"]:
                    product["quantity"] = product["quantity"] - stock
                    print("\nStock updated successfully!")
                    print("Remaining quantity:", product["quantity"])
                else:
                    print("Not enough stock available!")

        if found == False:
            print("Product not found!")

    elif choice == 5:
        product_name = input("Enter product name to search: ")
        found = False

        for product in products:
            if product["name"] == product_name:
                print("\nProduct Found!")
                print("Name     :", product["name"])
                print("Price    : ₹", product["price"])
                print("Quantity :", product["quantity"])
                found = True

        if found == False:
            print("Product not found!")

    elif choice == 6:
        print("\n========== LOW STOCK ALERT ==========")
        found = False

        for product in products:
            if product["quantity"] <= 5:
                print("Product :", product["name"])
                print("Stock   :", product["quantity"])
                print("------------------------------")
                found = True

        if found == False:
            print("No products are low in stock!")

    elif choice == 7:
        product_name = input("Enter product name: ")
        quantity_sold = int(input("Enter quantity sold: "))
        found = False

        for product in products:
            if product["name"] == product_name:
                found = True

                if quantity_sold <= product["quantity"]:
                    total_sale = product["price"] * quantity_sold
                    product["quantity"] = product["quantity"] - quantity_sold

                    print("\n========== SALE DETAILS ==========")
                    print("Product         :", product["name"])
                    print("Price           : ₹", product["price"])
                    print("Quantity Sold   :", quantity_sold)
                    print("Total Sale      : ₹", total_sale)
                    print("Remaining Stock :", product["quantity"])
                else:
                    print("Not enough stock available!")

        if found == False:
            print("Product not found!")

    elif choice == 8:
        print("\nThank you for using Inventory Management System!")
        break

    else:
        print("\nInvalid choice!")
