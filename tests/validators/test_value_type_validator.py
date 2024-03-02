from math import inf

from pyorlib.validators import ValueTypeValidator


class TestValueTypeValidator:

    def test_binary_value_type_validator(self):
        assert ValueTypeValidator.is_binary(0)
        assert ValueTypeValidator.is_binary(1)

        # Validate non binary numbers
        assert not ValueTypeValidator.is_binary(-1)
        assert not ValueTypeValidator.is_binary(-0.1)
        assert not ValueTypeValidator.is_binary(1.1)
        assert not ValueTypeValidator.is_binary(10)
        assert not ValueTypeValidator.is_binary(inf)
        assert not ValueTypeValidator.is_binary(-inf)
        assert not ValueTypeValidator.is_binary(None)

    def test_integer_value_type_validator(self):
        assert ValueTypeValidator.is_integer(5)
        assert ValueTypeValidator.is_integer(-80)
        assert ValueTypeValidator.is_integer(0)
        assert ValueTypeValidator.is_integer(inf)
        assert ValueTypeValidator.is_integer(-inf)

        # Validate non binary numbers
        assert not ValueTypeValidator.is_integer(-0.1)
        assert not ValueTypeValidator.is_integer(1.1)
        assert not ValueTypeValidator.is_integer(None)
