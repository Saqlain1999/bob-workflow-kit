"""Public behavioural regression checks for the deliberately faulty fixture."""

import unittest

from ledger import Ledger, LedgerError


class LedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = Ledger()
        self.ledger.open_account("alice", 1250)
        self.ledger.open_account("bob", 500)

    def test_account_creation_rejects_invalid_opening_values(self) -> None:
        before = self.ledger.snapshot()
        for value in (-1, 1.5, True, "100"):
            with self.subTest(value=value):
                with self.assertRaises(LedgerError):
                    self.ledger.open_account("new", value)
                self.assertEqual(self.ledger.snapshot(), before)

    def test_duplicate_account_preserves_its_balance(self) -> None:
        before = self.ledger.snapshot()
        with self.assertRaises(LedgerError):
            self.ledger.open_account("alice", 0)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_transfer_updates_both_accounts_and_conserves_total(self) -> None:
        before_total = sum(self.ledger.snapshot().values())
        self.ledger.transfer("alice", "bob", 175)
        self.assertEqual(self.ledger.balance("alice"), 1075)
        self.assertEqual(self.ledger.balance("bob"), 675)
        self.assertEqual(sum(self.ledger.snapshot().values()), before_total)

    def test_unknown_source_leaves_balances_unchanged(self) -> None:
        before = self.ledger.snapshot()
        with self.assertRaises(LedgerError):
            self.ledger.transfer("missing", "bob", 175)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_unknown_destination_leaves_balances_unchanged(self) -> None:
        before = self.ledger.snapshot()
        with self.assertRaises(LedgerError):
            self.ledger.transfer("alice", "missing", 175)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_insufficient_funds_leave_balances_unchanged(self) -> None:
        before = self.ledger.snapshot()
        with self.assertRaises(LedgerError):
            self.ledger.transfer("alice", "bob", 2000)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_invalid_transfer_amounts_leave_balances_unchanged(self) -> None:
        before = self.ledger.snapshot()
        for value in (-1, 0, 1.5, True, "100"):
            with self.subTest(value=value):
                with self.assertRaises(LedgerError):
                    self.ledger.transfer("alice", "bob", value)
                self.assertEqual(self.ledger.snapshot(), before)

    def test_same_account_transfer_is_rejected(self) -> None:
        before = self.ledger.snapshot()
        with self.assertRaises(LedgerError):
            self.ledger.transfer("alice", "alice", 175)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_snapshot_does_not_expose_internal_balances(self) -> None:
        snapshot = self.ledger.snapshot()
        snapshot["alice"] = 0
        snapshot["new"] = 100
        self.assertEqual(self.ledger.snapshot(), {"alice": 1250, "bob": 500})


if __name__ == "__main__":
    unittest.main()
