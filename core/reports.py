from datetime import datetime


def category_report(transactions):
    report = _expense_totals_by_category(transactions)

    result = ""

    for category, amount in report.items():
        result += f"{category}: ₹{amount}\n"

    if result == "":
        result = "no expense data available"

    return result


def top_category(transactions):
    categories = _expense_totals_by_category(transactions)

    if not categories:
        return "None"

    return max(categories, key=categories.get)


def monthly_expense(transactions):
    month = datetime.now().month

    total = 0

    for transaction in transactions:
        if transaction["type"] == "Expense":
            date = datetime.strptime(
                transaction["date"],
                "%d-%m-%Y %H:%M"
            )

            if date.month == month:
                total += transaction["amount"]

    return f"₹{total:,.0f}"


def expense_summary(transactions):
    summary = _expense_totals_by_category(transactions)

    result = ""

    for category, amount in summary.items():
        result += f"{category}: ₹{amount}\n"

    return result


def category_statistics(transactions):
    stats = {}

    for transaction in transactions:
        if transaction["type"] != "Expense":
            continue

        category = transaction["category"]

        if category not in stats:
            stats[category] = {
                "total": 0,
                "months": set()
            }

        stats[category]["total"] += transaction["amount"]

        date_obj = datetime.strptime(
            transaction["date"],
            "%d-%m-%Y %H:%M"
        )

        month_key = f"{date_obj.year}-{date_obj.month}"

        stats[category]["months"].add(month_key)

    expenses = [
        transaction for transaction in transactions
        if transaction["type"] == "Expense"
    ]

    incomes = [
        transaction for transaction in transactions
        if transaction["type"] == "Income"
    ]

    highest_expense = (
        max(expenses, key=lambda transaction: transaction["amount"])
        if expenses else None
    )

    highest_income = (
        max(incomes, key=lambda transaction: transaction["amount"])
        if incomes else None
    )

    avg_expense = (
        sum(transaction["amount"] for transaction in expenses)
        / len(expenses)
        if expenses else 0
    )

    avg_income = (
        sum(transaction["amount"] for transaction in incomes)
        / len(incomes)
        if incomes else 0
    )

    result = (
        "📊 FINANCE STATISTICS\n\n"
        f"Total Transactions: "
        f"{len(transactions)}\n\n"
    )

    if highest_expense:
        result += (
            "Highest Expense:\n"
            f"{highest_expense['category']} "
            f"₹{highest_expense['amount']:.0f}\n\n"
        )

    if highest_income:
        result += (
            "Highest Income:\n"
            f"{highest_income['category']} "
            f"₹{highest_income['amount']:.0f}\n\n"
        )

    result += (
        f"Average Expense: "
        f"₹{avg_expense:.0f}\n"
        f"Average Income: "
        f"₹{avg_income:.0f}\n"
        f"Expense Categories: "
        f"{len(stats)}\n\n"
        "-----------------------------\n\n"
    )

    for category, data in stats.items():
        total = data["total"]
        months = len(data["months"])

        avg_monthly = (
            total / months
            if months else 0
        )

        result += (
            f"{category}\n"
            f"Total Expense: ₹{total:.0f}\n"
            f"Months Active: {months}\n"
            f"Average Monthly Expense: "
            f"₹{avg_monthly:.0f}\n\n"
        )

    return result


def _expense_totals_by_category(transactions):
    totals = {}

    for transaction in transactions:
        if transaction["type"] == "Expense":
            category = transaction["category"]
            totals[category] = (
                totals.get(category, 0)
                + transaction["amount"]
            )

    return totals

def highest_expense(transactions):
    expenses = [
        t for t in transactions
        if t["type"] == "Expense"
    ]

    if not expenses:
        return "None", "₹0"

    highest = max(
        expenses,
        key=lambda t: t["amount"]
    )

    return (
        highest["category"],
        f"₹{highest['amount']:.0f}"
    )


def highest_income(transactions):
    incomes = [
        t for t in transactions
        if t["type"] == "Income"
    ]

    if not incomes:
        return "None", "₹0"

    highest = max(
        incomes,
        key=lambda t: t["amount"]
    )

    return (
        highest["category"],
        f"₹{highest['amount']:.0f}"
    )
