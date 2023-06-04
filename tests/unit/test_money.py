"""Tests for Money Class"""

# Standard libraries import

# Third party libraries import
import pytest

# Project import
from src.currency.money import (
    Symbol,
    Money,
    InvalidMoneyType,
)


@pytest.fixture
def symbol_enum() -> Symbol:
    """Returns an object from the symbol string enumeration class"""
    return Symbol("EUR")


class TestDummyImports:
    """Class that contains dummy tests to check out-of-package functionality"""

    def test_import_are_working_fine(self):
        """Dummy test to check whether or not imports from
        src are woking or not"""
        pass


class TestSymbolStrEnum:
    """Class that contains the tests for the Symbol String Enumeration Class"""

    def test_len_symbol(self):
        assert len(Symbol) == 23


class TestMoneyClass:
    """Class that contains the tests for the Money Class"""

    def test_money_init_method(self):
        """__init__() should return a valid object with correct
        digits and precision"""
        # GIVEN an initialized money object
        # WHEN the digits and precision are queried
        # THEN returned correct values
        money = Money(200, 2)
        assert money.digits == 1
        assert money.precision == 2

    @pytest.mark.parametrize('actual, expected',
                             [(Money(100, 2) + Money(200, 2), 300),
                              (Money(200, 2) + Money(200, 2), 400),
                              (Money(-100, 2) + Money(300, 2), 200),
                              (Money(-200, 2) + Money(-100, 2), -300),
                              (Money(400, 2) + Money(200, 2), 600),
                              (Money(100, 2) + Money(1200, 2), 1300),
                              (Money(400, 2) + Money(250, 2), 650),
                              ])  # type: ignore
    def test_sum_provides_correct_result(self, 
                                         actual: Money, 
                                         expected: int):
        assert actual.amount_cents == expected

    @pytest.mark.parametrize('actual, expected',
                             [(Money(100, 2) - Money(200, 2), -100),
                              (Money(200, 2) - Money(200, 2), 0),
                              (Money(100, 2) - Money(300, 2), -200),
                              (Money(200, 2) - Money(100, 2), 100),
                              (Money(400, 2) - Money(200, 2), 200),
                              (Money(100, 2) - Money(1200, 2), -1100),
                              (Money(400, 2) - Money(250, 2), 150),
                              ])  # type: ignore
    def test_subtraction_provides_correct_result(self,
                                                 actual: Money,
                                                 expected: int):
        assert actual.amount_cents == expected

    def test_sum_of_money_with_other_type_raises_InvalidMoneyTypeError(self):
        money1 = Money(100, 2)
        other = 2
        with pytest.raises(InvalidMoneyType) as ex:
            money1 + other  # type: ignore
        assert ex.type == InvalidMoneyType
        assert ex.value.args[0] == "Invalid Money Type"
