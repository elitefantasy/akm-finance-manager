from datetime import datetime
from core.icons import Icons

CATEGORY_ICONS = {
    "Food": Icons.FOOD,
    "Travel": Icons.TRAVEL,
    "Shopping": Icons.SHOPPING,
    "Medical": Icons.MEDICAL,
    "Education": Icons.EDUCATION,
    "Other": Icons.OTHER,
}

class TransactionFormatter:

    @staticmethod
    def category_icon(transaction):
        return CATEGORY_ICONS.get(
            transaction["category"],
            Icons.OTHER
        )

    @staticmethod
    def amount(transaction):
        """Return formatted amount with sign and commas."""

        sign = "+" if transaction["type"] == "Income" else "-"

        return f"{sign}₹{transaction['amount']:,.0f}"

    @staticmethod
    def amount_color(transaction):
        """Return Kivy RGBA color."""

        if transaction["type"] == "Income":
            return [0, 1, 0, 1]

        return [1, 0.3, 0.3, 1]

    @staticmethod
    def note(transaction):
        """Return note or default placeholder."""

        note = transaction.get("note", "").strip()

        return note if note else "No Note"

    @staticmethod
    def date(transaction):
        """Return formatted date."""

        try:
            dt = datetime.strptime(
                transaction["date"],
                "%d-%m-%Y %H:%M"
            )

            return dt.strftime("%d %b %Y")

        except Exception:
            return transaction["date"].split()[0]

    @staticmethod
    def history(transaction):
        """Return formatted data for History screen."""

        return {
            "category": transaction["category"],
            "amount": TransactionFormatter.amount(transaction),
            "note": TransactionFormatter.note(transaction),
            "date": TransactionFormatter.date(transaction),
            "amount_color": TransactionFormatter.amount_color(transaction),
            "transaction_id": transaction["id"],
        }