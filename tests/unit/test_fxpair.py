"""Tests for FXPair Class"""

# Standard libraries import

# Third party libraries import
import pytest

# Project import
from src.currency.money import (
    Symbol,    
)
from src.currency.forexpair import (
    FXPair,
    InvalidFXPair
)


class TestDummyImports:
    """Class that contains dummy tests to check out-of-package functionality"""

    def test_import_are_working_fine(self):
        """Dummy test to check whether or not imports from
        src are woking or not"""
        pass


class TestFXPairClass:
    """ Class that contains tests for FXPair class """
    def test_fx_pair(self):
        """__init__() should return a valid object with correct
        base and quote currencies"""
        # GIVEN an initialized money object
        # WHEN the digits and precision are queried
        # THEN returned correct values
        base = Symbol("EUR")
        quote = Symbol("USD")
        eurusd = FXPair(base, quote, 5)
        assert str(eurusd) == f"{str(base)}{str(quote)}"

    def test_fx_raises_InvalidFXTypeError(self):
        base = quote = Symbol("EUR")
        with pytest.raises(InvalidFXPair) as exc:
            FXPair(base, quote, 5)
        assert exc.type == InvalidFXPair
        assert exc.value.args[0] ==\
            "Base and quote currencies must be different"
