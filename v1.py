# Mobile Recharge Simulator


# Recharge plans for different operators
plans = {
    "Jio": [
        {"price": 199, "validity": 23, "data": "1.5 GB/day"},
        {"price": 299, "validity": 28, "data": "1.5 GB/day"},
        {"price": 399, "validity": 28, "data": "2.5 GB/day"}
    ],

    "Airtel": [
        {"price": 199, "validity": 23, "data": "2 GB/day"},
        {"price": 299, "validity": 28, "data": "1.5 GB/day"},
        {"price": 349, "validity": 28, "data": "2.5 GB/day"}
    ],

    "Vi": [
        {"price": 199, "validity": 23, "data": "1 GB/day"},
        {"price": 299, "validity": 28, "data": "1.5 GB/day"},
        {"price": 399, "validity": 28, "data": "2.5 GB/day"}
    ],

    "BSNL": [
        {"price": 187, "validity": 30, "data": "1 GB/day"},
        {"price": 247, "validity": 30, "data": "1.5 GB/day"},
        {"price": 397, "validity": 30, "data": "2 GB/day"}
    ]
}


def get_mobile_number():
    """Get and validate the user's mobile number."""

    while True:
        mobile_number = input("Enter your mobile number: ")

        if mobile_number.isdigit() and len(mobile_number) == 10:
            return mobile_number

        print("Invalid mobile number!")
        print("Please enter a valid 10-digit number.\n")


def choose_operator():
    """Display operators and return the selected operator."""

    operators = list(plans.keys())

    print("\nSelect your operator:")
    
    for number, operator in enumerate(operators, start=1):
        print(f"{number}. {operator}")

    while True:
        choice = input("Enter your choice: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(operators):
                return operators[choice - 1]

        print("Invalid choice! Please select a valid operator.")


def show_plans(operator):
    """Display recharge plans for the selected operator."""

    print(f"\n---------- {operator.upper()} RECHARGE PLANS ----------")

    operator_plans = plans[operator]

    for number, plan in enumerate(operator_plans, start=1):
        print(
            f"{number}. ₹{plan['price']} - "
            f"{plan['validity']} Days - "
            f"{plan['data']}"
        )


def choose_plan(operator):
    """Allow the user to select a recharge plan."""

    operator_plans = plans[operator]

    while True:
        choice = input("\nSelect a plan: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(operator_plans):
                return operator_plans[choice - 1]

        print("Invalid choice! Please select a valid plan.")


def confirm_recharge(mobile_number, operator, plan):
    """Display recharge details and ask for confirmation."""

    print("\n---------- RECHARGE DETAILS ----------")
    print(f"Mobile Number : {mobile_number}")
    print(f"Operator      : {operator}")
    print(f"Plan          : ₹{plan['price']}")
    print(f"Validity      : {plan['validity']} Days")
    print(f"Data          : {plan['data']}")

    while True:
        confirmation = input("\nConfirm recharge? (Y/N): ").strip().lower()

        if confirmation == "y":
            return True

        if confirmation == "n":
            return False

        print("Please enter Y or N.")


def process_recharge():
    """Handle the complete recharge process."""

    print("\n========================================")
    print("       MOBILE RECHARGE SIMULATOR")
    print("========================================")

    mobile_number = get_mobile_number()
    operator = choose_operator()

    show_plans(operator)
    plan = choose_plan(operator)

    confirmed = confirm_recharge(mobile_number, operator, plan)

    if confirmed:
        print("\nProcessing recharge...")
        print("\n========================================")
        print("       RECHARGE SUCCESSFUL!")
        print("========================================")
        print(f"Mobile Number : {mobile_number}")
        print(f"Amount        : ₹{plan['price']}")
        print(f"Operator      : {operator}")
        print(f"Validity      : {plan['validity']} Days")
        print(f"Data          : {plan['data']}")
    else:
        print("\nRecharge cancelled.")


def main():
    """Start the mobile recharge simulator."""

    process_recharge()


main()