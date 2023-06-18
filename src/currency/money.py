"""Class Money"""
# Standard Library imports
from datetime import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self
from enum import StrEnum

# Third party imports
# TODO: Remove dependency from this, better Google/Yahoo
from forex_python.converter import CurrencyRates


class Symbol(StrEnum):
    """Enumeration that represents the currency symbol

    Args:
        StrEnum (Symbol): Symbol for the currency

    Returns:
        StrEnum: Returns an Enumreation of type 'Symbol'
    """

    AUD = ("AUD",)
    BGN = ("BGN",)
    CAD = ("CAD",)
    CHF = ("CHF",)
    CZK = ("CZK",)
    DKK = ("DKK",)
    EUR = ("EUR",)
    GBP = ("GBP",)
    HKD = ("HKD",)
    HUF = ("HUF",)
    ILS = ("ILS",)
    JPY = ("JPY",)
    MXN = ("MXN",)
    NOK = ("NOK",)
    PLN = ("PLN",)
    RON = ("RON",)
    RUB = ("RUB",)
    SEK = ("SEK",)
    SGD = ("SGD",)
    TRY = ("TRY",)
    USD = ("USD",)
    NZD = ("NZD",)
    ZAR = ("ZAR",)

    def __str__(self) -> str:
        """Human-readable representation of the Symbol

        Returns:
            str: String with the Symbol
        """
        return f"{self.name}"

    def __len__(self) -> int:
        """The length of this class is the number of symbols it can support

        Returns:
            int: number of symbols supported
        """
        return len(Symbol.symbol_supported())

    @classmethod
    def symbol_supported(cls) -> list[str]:
        """Returns a list with all the Symbols suppported

        _extended_summary_

        Returns:
            list[str]: _description_
        """
        return list(cls.__members__.keys())


class InvalidMoneyType(Exception):
    """Raised when the type is not of Money type


    Args:
        Exception (InvalidMoneyType): Object type is not
        compliant to Money type
    """

    def __init__(self, msg: str = "Invalid Money Type") -> None:
        """Exception initializer

        Args:
            msg (str, optional): Error when object is not from Money type.
            Defaults to "Object type not compliant with Money type".
        """
        self.message = msg
        super().__init__(self.message)


def count_digits(num: int | float | Decimal) -> int:
    """Counts the number of digits in a given floating-point or Decimal number.

    Args:
        number: A float or Decimal number.

    Returns:
        The number of digits in the given number.

    Raises:
        ValueError: If the number is not of type float or Decimal.
    """
    if isinstance(num, float):
        digits = str(num).rstrip("0")
    elif isinstance(num, int):
        digits = str(num)
    elif isinstance(num, Decimal):  # type: ignore
        digits = num.normalize().to_eng_string().rstrip("0")

    else:
        raise ValueError("Number must be in Decimal, float or int format")

    if "." in digits:
        return len(digits) - 1  # Substract one to discard the decimal point
    else:
        return len(digits)


def count_decimals(num: int | float | Decimal):
    """Counts the total number of decimals in a given
        floating-point or Decimal number.

    Args:
        number: An int, float or Decimal number.

    Returns:
        The total number of decimals in the given number.

    Raises:
        ValueError: If the number is not of type float or Decimal.
    """
    if isinstance(num, float) or isinstance(num, int):
        dec = str(num)
    elif isinstance(num, Decimal):  # type: ignore
        dec = num.normalize().to_eng_string()
    else:
        raise ValueError("The number must be of type float or Decimal")

    if "." in dec:
        return len(dec.split(".")[-1])
    else:
        return 0


@dataclass(slots=True)
class Money:
    """Class to represent a currency and the corresponding value.

    This class can represent any currency with the precision
    specified by the `precision` attribute.

    Attributes:
        amount_cents (int): The value of the money in cents.
        precision (int): The decimal precision of the money.
        currency_symbol (Symbol): The symbol of the currency.
        digits (int): The number of digits in the amount_cents.

    Returns:
        Money: An instance of the Money class.
    """

    amount_cents: int
    precision: int = 2
    currency_symbol: Symbol = Symbol("EUR")
    digits: int = field(default_factory=int)

    def __post_init__(self) -> None:
        """Post_initialize the Money instance.

        This method is called after the instance has been initialized.
        It sets the number of digits in the `digits` attribute.
        """
        self.digits = count_digits(self.amount_cents / 10**self.precision)

    @classmethod
    def mint(
        cls, amount: Decimal | float, currency_symbol: Symbol = Symbol("EUR")
    ) -> Self:
        """Create a new Money instance.

        This method creates a new Money instance using the given `amount`
        and `currency_symbol`.The `precision` attribute is determined
        based on the number of decimals in the `amount`.

        Args:
            amount (Decimal or float): The value of the money.
            currency_symbol (Symbol, optional): The symbol of the currency.
            Defaults to "EUR".

        Returns:
            Money: A new instance of the Money class.
        """
        precision: int = count_decimals(amount)
        return cls(int(amount * (10**precision)), precision, currency_symbol)

    def convert_to(self, other_curr: Self, date_str: str) -> Self:
        # Date str to datetime object
        date_and_time = dt.strptime(date_str, "%Y-%m-%d").date()
        # Get the exchange rate using forex-python library
        c = CurrencyRates(force_decimal=True)
        exchange_rate: Decimal = \
            c.get_rate(str(self.currency_symbol),  # type: ignore
                       str(other_curr.currency_symbol),
                       date_and_time)  # type: ignore
        return Money(exchange_rate * self.amount_cents,  # type: ignore
                     self.precision,
                     other_curr.currency_symbol)

    def __str__(self) -> str:
        """Return a string representation of the Money instance.

        Returns:
            str: The string representation of the Money instance.
        """
        return f"{self.amount_cents / 100:.2f} {self.currency_symbol}"

    def __add__(self, other: Self) -> Self:
        """Add two Money instances.

        This method adds two Money instances together if they
        have the same currency symbol.

        Args:
            other (Money): The Money instance to be added.

        Returns:
            Money: The sum of the two Money instances.

        Raises:
            InvalidMoneyType: If the `other` parameter is not an
            instance of the Money class.
        """
        if (isinstance(other, Money)
                and self.currency_symbol == other.currency_symbol):
            return Money(
                self.amount_cents + other.amount_cents,
                self.precision,
                self.currency_symbol,
            )
        else:
            raise InvalidMoneyType()

    def __sub__(self, other: Self) -> Self:
        """Subtract two Money instances.

        This method subtracts the `other` Money instance from the current
        Money instance.

        Args:
            other (Money): The Money instance to be subtracted.

        Returns:
            Money: The difference between the two Money instances.

        Raises:
            InvalidMoneyType: If the `other` parameter is not an instance
            of the Money class.
        """
        if (isinstance(other, Money)
                and self.currency_symbol == other.currency_symbol):
            return Money(
                self.amount_cents - other.amount_cents,
                self.precision,
                self.currency_symbol,
            )
        else:
            raise InvalidMoneyType()
