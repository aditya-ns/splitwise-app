# ============================================================================
# SPLIT BILL CALCULATOR - A Splitwise-like Application
# ============================================================================
# This program helps split shared expenses among group members fairly.
# It calculates who owes money and who should receive money to settle debts.
# ============================================================================

def get_group_data():
    """
    Collect group data: number of people, their names, and amounts spent.
    
    Returns:
        tuple: (list of names, list of amounts spent)
    """
    # Get the number of people
    while True:
        try:
            n = int(input("\n==> Enter the number of people in the group: "))
            if n <= 0:
                print("    [ERROR] Number of people must be at least 1.")
                continue
            break
        except ValueError:
            print("    [ERROR] Please enter a valid integer.")

    names = []
    amounts = []

    print("\n==> Enter each person's name and the amount they spent:")
    for i in range(n):
        # Get person's name
        while True:
            name = input(f"    Person {i+1} name: ").strip()
            if name == "":
                print("    [ERROR] Name cannot be empty.")
                continue
            # Check for duplicate names
            if name in names:
                print(f"    [ERROR] '{name}' already entered. Please use a different name.")
                continue
            break
        names.append(name)

        # Get amount spent by this person
        while True:
            try:
                amount = float(input(f"    Amount spent by {name}: "))
                if amount < 0:
                    print("    [ERROR] Amount cannot be negative.")
                    continue
                break
            except ValueError:
                print("    [ERROR] Please enter a valid number.")
        amounts.append(amount)

    return names, amounts

def compute_balances(names, amounts):
    """
    Calculate total expense, per-person share, and individual balances.
    
    Args:
        names (list): List of person names
        amounts (list): List of amounts spent by each person
    
    Returns:
        tuple: (total_expense, equal_share, balances_dict)
        - balance > 0: person should receive money
        - balance < 0: person should pay money
    """
    total_expense = sum(amounts)
    n = len(names)
    equal_share = total_expense / n if n > 0 else 0.0

    # Calculate balance for each person
    # balance = amount_paid - equal_share
    balances = {}
    for name, amt in zip(names, amounts):
        balances[name] = round(amt - equal_share, 2)

    return total_expense, equal_share, balances

def settle_debts(balances):
    """
    Generate settlement transactions using a greedy algorithm.
    
    This algorithm minimizes the number of transactions by repeatedly
    matching the largest debtor with the largest creditor.
    
    Args:
        balances (dict): Dictionary mapping names to their balance
    
    Returns:
        list: List of tuples (payer, receiver, amount)
    """
    # Separate creditors (positive balance) and debtors (negative balance)
    creditors = []  # [name, amount to receive]
    debtors = []    # [name, amount to pay]

    for name, bal in balances.items():
        if bal > 0.01:  # Use small threshold to avoid floating point issues
            creditors.append([name, bal])
        elif bal < -0.01:
            debtors.append([name, -bal])  # Store positive value

    # Sort by amount (largest first) for greedy matching
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)

    transactions = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor_name, debtor_owes = debtors[i]
        creditor_name, creditor_receives = creditors[j]

        # Amount to settle in this transaction
        amount = round(min(debtor_owes, creditor_receives), 2)

        if amount > 0:
            transactions.append((debtor_name, creditor_name, amount))

        # Update remaining amounts
        debtor_owes = round(debtor_owes - amount, 2)
        creditor_receives = round(creditor_receives - amount, 2)

        debtors[i][1] = debtor_owes
        creditors[j][1] = creditor_receives

        # Move to next debtor/creditor if fully settled
        if debtor_owes < 0.01:
            i += 1
        if creditor_receives < 0.01:
            j += 1

    return transactions

def print_summary(names, amounts, total_expense, equal_share, balances, transactions):
    """
    Print a comprehensive summary of expenses and settlements.
    
    Args:
        names (list): List of person names
        amounts (list): List of amounts spent
        total_expense (float): Total expense
        equal_share (float): Equal share per person
        balances (dict): Balance for each person
        transactions (list): Settlement transactions
    """
    print("\n" + "="*70)
    print("GROUP EXPENSE SUMMARY & SETTLEMENT REPORT".center(70))
    print("="*70)

    # Section 1: Overall Summary
    print("\n[OVERALL SUMMARY]")
    print(f"  Total Expense: ₹{total_expense:.2f}")
    print(f"  Number of People: {len(names)}")
    print(f"  Equal Share per Person: ₹{equal_share:.2f}")

    # Section 2: Individual Spending
    print("\n[INDIVIDUAL SPENDING]")
    for name, amt in zip(names, amounts):
        print(f"  {name:20s} spent ₹{amt:10.2f}")

    # Section 3: Balance Sheet
    print("\n[BALANCE SHEET]")
    print(f"  {'Name':20s} {'Amount Paid':>15s} {'Equal Share':>15s} {'Balance':>15s}")
    print("  " + "-"*65)
    for name in names:
        amt = next(a for n, a in zip(names, amounts) if n == name)
        bal = balances[name]
        status = "(Receives)" if bal > 0 else "(Pays)" if bal < 0 else "(Even)"
        print(f"  {name:20s} {amt:15.2f} {equal_share:15.2f} {bal:+10.2f} {status}")

    # Section 4: Settlement Instructions
    print("\n[SETTLEMENT INSTRUCTIONS]")
    if not transactions:
        print("  ✓ Everyone is settled! No payments needed.")
    else:
        print(f"  Total transactions needed: {len(transactions)}\n")
        for idx, (payer, receiver, amount) in enumerate(transactions, 1):
            print(f"  {idx}. {payer} should pay {receiver} ₹{amount:.2f}")

    print("\n" + "="*70)

def main():
    """
    Main function: orchestrate the bill splitting process.
    """
    print("\n" + "#"*70)
    print("#" + " WELCOME TO SPLIT BILL CALCULATOR ".center(68) + "#")
    print("#"*70)

    # Step 1: Collect group data
    names, amounts = get_group_data()

    # Step 2: Calculate balances
    total_expense, equal_share, balances = compute_balances(names, amounts)

    # Step 3: Determine settlement transactions
    transactions = settle_debts(balances)

    # Step 4: Display summary
    print_summary(names, amounts, total_expense, equal_share, balances, transactions)


# ============================================================================
# PROGRAM EXECUTION
# ============================================================================

if __name__ == "__main__":
    main()