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
        """If a currency has the same base and quote symbol,
        it should raise an exception
        """
        # GIVEN a base and a quote currency
        # WHEN both have the same symbol
        # THEN raise an InvalidFXPair exception
        base = quote = Symbol("EUR")
        with pytest.raises(InvalidFXPair) as exc:
            FXPair(base, quote, 5)
        assert exc.type == InvalidFXPair
        assert exc.value.args[0] ==\
            "Base and quote currencies must be different"
            
    def test_swap_base_and_quote_currencies(self):
        """Base and Quote currencies are swaped over"""
        # GIVEN an FXPair object
        # WHEN swap is called
        # THEN base and quote currencies are swaped over
        fx_pair = FXPair(Symbol("USD"), Symbol("EUR"), 3)
        assert fx_pair.base_cur == Symbol("USD")
        assert fx_pair.quote_cur == Symbol("EUR")
        fx_pair.swap_base_and_quote()
        assert fx_pair.base_cur == Symbol("EUR")
        assert fx_pair.quote_cur == Symbol("USD")
