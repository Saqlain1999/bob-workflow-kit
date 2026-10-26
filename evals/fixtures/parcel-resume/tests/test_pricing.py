"""Public behavior checks; expected values come from the protected policy."""

import json
from pathlib import Path
import unittest

from parcel.pricing import quote


class PricingTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads(Path("policy.json").read_text(encoding="utf-8"))

    def test_below_policy_threshold_is_charged(self):
        subtotal = self.policy["free_delivery_min_cents"] - 1
        self.assertEqual(quote(subtotal)["delivery_cents"], self.policy["delivery_cents"])

    def test_at_policy_threshold_is_free(self):
        self.assertEqual(quote(self.policy["free_delivery_min_cents"])["delivery_cents"], 0)

    def test_small_quote_preserves_contract(self):
        self.assertEqual(quote(1100), {
            "currency": self.policy["currency"], "subtotal_cents": 1100,
            "delivery_cents": self.policy["delivery_cents"],
            "total_cents": 1100 + self.policy["delivery_cents"],
        })

    def test_zero_quote_uses_delivery_policy(self):
        result = quote(0)
        self.assertEqual(result["delivery_cents"], self.policy["delivery_cents"])
        self.assertEqual(result["total_cents"], self.policy["delivery_cents"])

    def test_invalid_subtotals_are_rejected(self):
        for value in (-1, True, 1.5, "200"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                quote(value)


if __name__ == "__main__":
    unittest.main()
