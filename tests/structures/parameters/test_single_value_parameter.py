from math import inf

from _pytest.python_api import raises

from pyorlib.enums import ParameterType, ValueType
from pyorlib.structures import SingleValueParameter, Parameter


class TestSingleValueParameter:

    def test_inheritance(self):
        assert issubclass(SingleValueParameter, Parameter)

    def test_parameter_type(self):
        # Validates FIXED parameters
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                lower_bound=1,
                upper_bound=4,
                value=2,
            )
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                lower_bound=1,
                upper_bound=4,
            )

        # Validates FIXED parameters
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bound=1,
                upper_bound=4,
                value=2,
            )
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                value=2,
            )

        # Validates None values
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=None,
                value_type=ValueType.INTEGER,
                value=2,
            )
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=None,
                value=2,
            )

    def test_creation_with_binary_value_type(self):
        # Validate FIXED SingleValueParameter
        param1 = SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.BINARY, value=0)

        assert param1 is not None
        assert not param1.is_bounded
        assert param1.value_type == ValueType.BINARY
        assert param1.parameter_type == ParameterType.FIXED
        assert param1.lower_bound is None and param1.upper_bound is None and param1.value is not None
        assert param1.value == 0

        # Validate Bounded SingleValueParameter
        param2 = SingleValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.BINARY,
            lower_bound=0,
            upper_bound=1,
        )

        assert param2 is not None
        assert param2.is_bounded
        assert param2.value_type == ValueType.BINARY
        assert param2.parameter_type == ParameterType.BOUNDED
        assert param2.lower_bound is not None and param2.upper_bound is not None and param2.value is None
        assert param2.lower_bound == 0 and param2.upper_bound == 1

        # Validates integer numbers
        with raises(ValueError):
            SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.BINARY, value=5)
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bound=0,
                upper_bound=2,
            )

        # Validates continuous numbers
        with raises(ValueError):
            SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.BINARY, value=5.2)

        # Validates lower and upper bounds
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bound=1,
                upper_bound=0,
            )

    def test_creation_with_integer_value_type(self):
        # Validate FIXED SingleValueParameter
        param1 = SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.INTEGER, value=80)

        assert param1 is not None
        assert not param1.is_bounded
        assert param1.value_type == ValueType.INTEGER
        assert param1.parameter_type == ParameterType.FIXED
        assert param1.lower_bound is None and param1.upper_bound is None and param1.value is not None
        assert param1.value == 80

        # Validate Bounded SingleValueParameter
        param2 = SingleValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.INTEGER,
            lower_bound=-1,
            upper_bound=10.0,
        )

        assert param2 is not None
        assert param2.is_bounded
        assert param2.value_type == ValueType.INTEGER
        assert param2.parameter_type == ParameterType.BOUNDED
        assert param2.lower_bound is not None and param2.upper_bound is not None and param2.value is None
        assert param2.lower_bound == -1 and param2.upper_bound == 10

        # Validates continuous numbers
        with raises(ValueError):
            SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.INTEGER, value=5.2)
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bound=0,
                upper_bound=2.1,
            )

        # Validates lower and upper bounds
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bound=-5,
                upper_bound=-20,
            )

    def test_creation_with_continuous_value_type(self):
        # Validate FIXED SingleValueParameter
        param1 = SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.CONTINUOUS, value=20.5)

        assert param1 is not None
        assert not param1.is_bounded
        assert param1.value_type == ValueType.CONTINUOUS
        assert param1.parameter_type == ParameterType.FIXED
        assert param1.lower_bound is None and param1.upper_bound is None and param1.value is not None
        assert param1.value == 20.5

        # Validate Bounded SingleValueParameter
        param2 = SingleValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.CONTINUOUS,
            lower_bound=5.6,
            upper_bound=5.7,
        )

        assert param2 is not None
        assert param2.is_bounded
        assert param2.value_type == ValueType.CONTINUOUS
        assert param2.parameter_type == ParameterType.BOUNDED
        assert param2.lower_bound is not None and param2.upper_bound is not None and param2.value is None
        assert param2.lower_bound == 5.6 and param2.upper_bound == 5.7

        # Validates infinities
        with raises(ValueError):
            SingleValueParameter(parameter_type=ParameterType.FIXED, value_type=ValueType.INTEGER, value=inf)

        # Validates infinities
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bound=-inf,
                upper_bound=inf,
            )

        # Validates lower and upper bounds
        with raises(ValueError):
            SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bound=-5,
                upper_bound=-20,
            )
