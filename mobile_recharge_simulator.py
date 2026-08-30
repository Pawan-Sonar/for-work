print("======================================")
print("       MOBILE RECHARGE SIMULATOR")
print("======================================")

mobile_number = input("Enter your mobile number: ")

if len(mobile_number) != 10 or not mobile_number.isdigit():
    print("Invalid mobile number!")
    print("Please enter a valid 10-digit mobile number.")
else:
    print("\nSelect your operator:")
    print("1. Jio")
    print("2. Airtel")
    print("3. Vi")
    print("4. BSNL")

    operator_choice = int(input("Enter your choice: "))

    if operator_choice == 1:
        operator = "Jio"
    elif operator_choice == 2:
        operator = "Airtel"
    elif operator_choice == 3:
        operator = "Vi"
    elif operator_choice == 4:
        operator = "BSNL"
    else:
        operator = ""

    if operator == "":
        print("Invalid operator choice!")
    else:
        print("\n--------------------------------------")
        print(operator, "Recharge Plans")
        print("--------------------------------------")

        print("1. ₹199 - 23 Days - 1.5 GB/day")
        print("2. ₹299 - 28 Days - 1.5 GB/day")
        print("3. ₹399 - 28 Days - 2.5 GB/day")

        plan_choice = int(input("Select a plan: "))

        if plan_choice == 1:
            price = 199
            validity = 23
            data = "1.5 GB/day"
        elif plan_choice == 2:
            price = 299
            validity = 28
            data = "1.5 GB/day"
        elif plan_choice == 3:
            price = 399
            validity = 28
            data = "2.5 GB/day"
        else:
            price = 0

        if price == 0:
            print("Invalid plan choice!")
        else:
            print("\n======================================")
            print("          RECHARGE DETAILS")
            print("======================================")

            print("Mobile Number :", mobile_number)
            print("Operator      :", operator)
            print("Amount        : ₹", price)
            print("Validity      :", validity, "Days")
            print("Data          :", data)

            confirmation = input("\nDo you want to recharge? (Y/N): ")

            if confirmation == "Y" or confirmation == "y":
                print("\nProcessing recharge...")
                print("\n======================================")
                print("       RECHARGE SUCCESSFUL!")
                print("======================================")

                print("Mobile Number :", mobile_number)
                print("Operator      :", operator)
                print("Amount        : ₹", price)
                print("Validity      :", validity, "Days")
                print("Data          :", data)
            elif confirmation == "N" or confirmation == "n":
                print("\nRecharge cancelled.")
            else:
                print("\nInvalid choice.")
                print("Recharge cancelled.")

print("\nThank you for using Mobile Recharge Simulator!")
