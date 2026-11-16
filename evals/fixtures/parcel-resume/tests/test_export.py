"""Public CSV checks against the workspace's protected delivery policy."""

import csv
import io
import json
from pathlib import Path
import unittest

from parcel.export import export_quotes


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads(Path("policy.json").read_text(encoding="utf-8"))

    def rows(self, values):
        return list(csv.DictReader(io.StringIO(export_quotes(values))))

    def test_below_policy_threshold_is_charged(self):
        result = self.rows([("below", self.policy["free_delivery_min_cents"] - 1)])
        self.assertEqual(int(result[0]["delivery_cents"]), self.policy["delivery_cents"])

    def test_at_policy_threshold_is_free(self):
        result = self.rows([("at", self.policy["free_delivery_min_cents"])])
        self.assertEqual(int(result[0]["delivery_cents"]), 0)

    def test_rows_keep_order_and_arithmetic(self):
        result = self.rows([("small, quoted", 1100), ("large", 10000)])
        self.assertEqual([row["reference"] for row in result], ["small, quoted", "large"])
        self.assertEqual(int(result[0]["total_cents"]), 1100 + self.policy["delivery_cents"])
        self.assertEqual(int(result[1]["total_cents"]), 10000)
        for row in result:
            self.assertEqual(int(row["total_cents"]), int(row["subtotal_cents"]) + int(row["delivery_cents"]))

    def test_empty_input_keeps_columns(self):
        self.assertEqual(export_quotes([]), "reference,subtotal_cents,delivery_cents,total_cents\n")

    def test_invalid_subtotals_are_rejected(self):
        for value in (-1, True, 1.5, "200"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                export_quotes([("invalid", value)])


if __name__ == "__main__":
    unittest.main()
