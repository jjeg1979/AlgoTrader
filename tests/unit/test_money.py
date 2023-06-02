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


class TestDummy:
    """Class that contains dummy tests to check out-of-package functionality"""
    
    def test_import_are_working_fine(self):
        """Dummy test to check whether or not imports from src are woking or not"""
        pass


class TestSymbol:
    """Class that contains the tests for the Symbol String Enumeration Class"""
        
    def test_len_symbol(self):
        assert len(Symbol) == 23


class MoneyTest:
    """Class that contains the tests for the Money Class"""
    pass