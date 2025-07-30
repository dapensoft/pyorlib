from math import inf

from pytest import raises

from pyorlib.algebra import Term, Constant
from pyorlib.enums import ValueType, TermType


class TestConstant:

    def test_inheritance(self):
        assert issubclass(Constant, Term)

    def test_binary_constant_creation(self):
        # Validates 0 constant
        constant_name_1: str = "c_1"
        const1: Constant = Constant(name=constant_name_1, value_type=ValueType.BINARY, value=0)

        assert const1 is not None
        assert isinstance(const1, Constant)
        assert const1.name == constant_name_1
        assert const1.term_type == TermType.CONSTANT
        assert const1.value_type == ValueType.BINARY
        assert const1.value == const1.lower_bound == const1.upper_bound == const1.raw == 0
        assert not const1.is_variable
        assert const1.is_constant

        # Validates 1 constant
        constant_name_2: str = "c_2"
        const2: Constant = Constant(name=constant_name_2, value_type=ValueType.BINARY, value=1)
        assert const2 is not None

        # Validates constants name
        with raises(Exception):
            Constant(name="", value_type=ValueType.BINARY, value=0)

        # Validates None values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.BINARY, value=None)

        # Validates constants with negative values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.BINARY, value=-1)

        # Validates constants with integer values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.BINARY, value=3)

        # Validates constants with continuous values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.BINARY, value=6.9)

        # Validates constants with infinity
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.BINARY, value=inf)

    def test_integer_constant_creation(self):
        # Validates integer constant
        constant_name_1: str = "c_1"
        const1: Constant = Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=-5)

        assert const1 is not None
        assert isinstance(const1, Constant)
        assert const1.name == constant_name_1
        assert const1.term_type == TermType.CONSTANT
        assert const1.value_type == ValueType.INTEGER
        assert const1.value == const1.lower_bound == const1.upper_bound == const1.raw == -5
        assert not const1.is_variable
        assert const1.is_constant

        # Validates empty name
        with raises(Exception):
            Constant(name="", value_type=ValueType.INTEGER, value=-5)

        # Validates None values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=None)

        # Validates constants with -infinity
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=-inf)

        # Validates constants with +infinity
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=inf)

        # Validates constants with continuous values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=3.3)

    def test_continuous_constant_creation(self):
        # Validates continuous constant
        constant_name_1: str = "c_1"
        const1: Constant = Constant(name=constant_name_1, value_type=ValueType.CONTINUOUS, value=5.3)

        assert const1 is not None
        assert isinstance(const1, Constant)
        assert const1.name == constant_name_1
        assert const1.term_type == TermType.CONSTANT
        assert const1.value_type == ValueType.CONTINUOUS
        assert const1.value == const1.lower_bound == const1.upper_bound == const1.raw == 5.3
        assert not const1.is_variable
        assert const1.is_constant

        # Validates integer values
        constant_name_2: str = "c_2"
        const2 = Constant(name=constant_name_2, value_type=ValueType.CONTINUOUS, value=5)
        assert const2 is not None

        # Validates empty name
        with raises(Exception):
            Constant(name="", value_type=ValueType.CONTINUOUS, value=5.3)

        # Validates None values
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.CONTINUOUS, value=None)

        # Validates -infinity
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.CONTINUOUS, value=-inf)

        # Validates +infinity
        with raises(Exception):
            Constant(name=constant_name_1, value_type=ValueType.INTEGER, value=inf)
