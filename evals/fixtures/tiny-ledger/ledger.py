"""An in-memory transfer exercise; balances are integer cents.

This learning fixture deliberately contains a bug. See README.md for its
behavioural contract and test instructions.
"""

from typing import Dict


class LedgerError(ValueError):
    """An operation does not satisfy the ledger's public contract."""


class Ledger:
    def __init__(self) -> None:
        self._balances: Dict[str, int] = {}

    def open_account(self, name: str, opening_cents: int = 0) -> None:
        self._validate_name(name)
        self._validate_cents(opening_cents, positive=False)
        if name in self._balances:
            raise LedgerError("Account already exists")
        self._balances[name] = opening_cents

    def balance(self, name: str) -> int:
        self._validate_name(name)
        if name not in self._balances:
            raise LedgerError("Unknown account")
        return self._balances[name]

    def snapshot(self) -> Dict[str, int]:
        return dict(self._balances)

    def transfer(self, source: str, destination: str, cents: int) -> None:
        self._validate_cents(cents, positive=True)
        if source == destination:
            raise LedgerError("Choose two different accounts")

        source_balance = self.balance(source)
        if source_balance < cents:
            raise LedgerError("Insufficient funds")

        self._balances[source] = source_balance - cents
        destination_balance = self.balance(destination)
        self._balances[destination] = destination_balance + cents

    @staticmethod
    def _validate_name(name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise LedgerError("Account name must be a non-empty string")

    @staticmethod
    def _validate_cents(cents: int, *, positive: bool) -> None:
        if isinstance(cents, bool) or not isinstance(cents, int):
            raise LedgerError("Balance and amount values must be integer cents")
        if cents < 0 or (positive and cents == 0):
            raise LedgerError("Amount is outside the permitted range")
