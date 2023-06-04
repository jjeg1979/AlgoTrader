"""Class ForexPair"""
# Standard library imports
from dataclasses import dataclass


# Third party imports

# Project imports
from src.currency.money import Symbol


class InvalidFXPair(Exception):
    """Raised when the base and quote currency are the same


    Args:
        Exception (InvalidFXPair): Object type is not
        compliant to FXPair type
    """

    def __init__(self, msg: str =
                 "Base and quote currencies must be different") -> None:
        """Exception initializer

        Args:
            msg (str, optional): Error when both currencies are the same.
            Defaults to "Base and quote currencies must be different".
        """
        self.message = msg
        super().__init__(self.message)


@dataclass(slots=True)
class FXPair:
    """Represents an FX Currency Pair"""
    base_cur: Symbol
    quote_cur: Symbol
    pip_size: int

    def __init__(self, base_cur: Symbol, 
                 quote_cur: Symbol, 
                 pip_size: int) -> None:
        if base_cur == quote_cur:
            raise InvalidFXPair()
        self.base_cur = base_cur
        self.quote_cur = quote_cur
        self.pip_size = pip_size

    def __str__(self):
        return f"{str(self.base_cur)}{str(self.quote_cur)}"
