from collections import defaultdict
from datetime import datetime


def expense_summary(transactions):
    income = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "Income"
    )

    expense = sum(
        t["amount"]
        for t in transactions
        if t["type"] == "Expense"
    )

    return (
        f"Income : ₹{income:,.0f}\n"
        f"Expense : ₹{expense:,.0f}\n"
        f"Balance : ₹{income-expense:,.0f}"
    )


def top_category(transactions):

    totals = defaultdict(float)

    for t in transactions:

        if t["type"] == "Expense":
            totals[t["category"]] += t["amount"]

    if not totals:
        return "None"

    return max(
        totals,
        key=totals.get
    )


def monthly_expense(transactions):

    now = datetime.now()

    total = 0

    for t in transactions:

        if t["type"] != "Expense":
            continue

        try:
            date = datetime.strptime(
                t["date"],
                "%d-%m-%Y %H:%M"
            )

            if (
                date.month == now.month
                and date.year == now.year
            ):
                total += t["amount"]

        except Exception:
            continue

    return f"₹{total:,.0f}"


def category_report(transactions):

    totals = defaultdict(float)

    for t in transactions:

        if t["type"] == "Expense":
            totals[t["category"]] += t["amount"]

    if not totals:
        return "No expense data."

    lines = []

    for category, amount in sorted(totals.items()):

        lines.append(
            f"{category}: ₹{amount:,.0f}"
        )

    return "\n".join(lines)


# =====================================================
# Statistics
# =====================================================

def statistics_data(transactions):

    stats = {}

    income = [
        t for t in transactions
        if t["type"] == "Income"
    ]

    expense = [
        t for t in transactions
        if t["type"] == "Expense"
    ]

    stats["balance"] = (
        sum(t["amount"] for t in income)
        - sum(t["amount"] for t in expense)
    )

    stats["income"] = sum(
        t["amount"]
        for t in income
    )

    stats["expense"] = sum(
        t["amount"]
        for t in expense
    )

    stats["transactions"] = len(
        transactions
    )

    stats["highest_income"] = (
        max(
            (t["amount"] for t in income),
            default=0
        )
    )

    stats["highest_expense"] = (
        max(
            (t["amount"] for t in expense),
            default=0
        )
    )

    stats["top_category"] = top_category(
        transactions
    )

    category_data = {}

    for t in expense:

        category = t["category"]

        if category not in category_data:

            category_data[category] = {
                "total": 0,
                "months": set(),
            }

        category_data[category]["total"] += t["amount"]

        try:

            date = datetime.strptime(
                t["date"],
                "%d-%m-%Y %H:%M"
            )

            category_data[category]["months"].add(
                (
                    date.month,
                    date.year,
                )
            )

        except Exception:
            pass

    categories = []

    for category, values in sorted(
        category_data.items()
    ):

        months = max(
            1,
            len(values["months"])
        )

        categories.append({

            "category": category,

            "total": values["total"],

            "months": months,

            "average": (
                values["total"] / months
            ),

        })

    stats["categories"] = categories

    stats["category_count"] = len(
        categories
    )

    return stats


# backward compatibility
def category_statistics(transactions):

    stats = statistics_data(
        transactions
    )

    if stats["transactions"] == 0:

        return (
            "No transaction data available."
        )

    result = []

    result.append(
        f"Balance : ₹{stats['balance']:,.0f}"
    )

    result.append(
        f"Income : ₹{stats['income']:,.0f}"
    )

    result.append(
        f"Expense : ₹{stats['expense']:,.0f}"
    )

    result.append(
        f"Transactions : {stats['transactions']}"
    )

    result.append(
        f"Highest Income : ₹{stats['highest_income']:,.0f}"
    )

    result.append(
        f"Highest Expense : ₹{stats['highest_expense']:,.0f}"
    )

    result.append(
        f"Top Category : {stats['top_category']}"
    )

    result.append("")

    for category in stats["categories"]:

        result.append(
            f"{category['category']}"
        )

        result.append(
            f"  Total : ₹{category['total']:,.0f}"
        )

        result.append(
            f"  Months : {category['months']}"
        )

        result.append(
            f"  Avg / Month : ₹{category['average']:,.0f}"
        )

        result.append("")

    return "\n".join(result)