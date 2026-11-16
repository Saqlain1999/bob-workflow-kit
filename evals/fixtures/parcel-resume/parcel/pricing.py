"""Return a quote using integer cents."""

from .policy import read_policy


def quote(subtotal_cents):
    if type(subtotal_cents) is not int or subtotal_cents < 0:
        raise ValueError("subtotal_cents must be a nonnegative integer")
    policy = read_policy()
    delivery_cents = 0 if subtotal_cents >= 5000 else policy["delivery_cents"]
    return {
        "currency": policy["currency"],
        "subtotal_cents": subtotal_cents,
        "delivery_cents": delivery_cents,
        "total_cents": subtotal_cents + delivery_cents,
    }
