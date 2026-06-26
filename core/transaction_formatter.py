from datetime import datetime


class TransactionFormatter:
    @staticmethod
    def amount(transaction):
        """Return formatted amount with sign."""

        sign = "+" if transaction["type"] == "Income" else "-"

        return f"{sign}₹{transaction['amount']:.0f}"

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
        """Return only the date portion."""

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