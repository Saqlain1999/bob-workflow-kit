"""Export reference/subtotal pairs as a CSV string."""

import csv
import io

from .policy import read_policy


def export_quotes(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("reference", "subtotal_cents", "delivery_cents", "total_cents"))
    policy = read_policy()
    for reference, subtotal_cents in rows:
        if type(subtotal_cents) is not int or subtotal_cents < 0:
            raise ValueError("subtotal_cents must be a nonnegative integer")
        delivery_cents = 0 if subtotal_cents >= 5000 else policy["delivery_cents"]
        writer.writerow((reference, subtotal_cents, delivery_cents, subtotal_cents + delivery_cents))
    return output.getvalue()
