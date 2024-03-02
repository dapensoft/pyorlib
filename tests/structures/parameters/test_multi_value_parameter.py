from math import inf

from _pytest.python_api import raises

from pyorlib.enums import ParameterType, ValueType
from pyorlib.structures import MultiValueParameter, Parameter


class TestMultiValueParameter:

    def test_inheritance(self):
        assert issubclass(MultiValueParameter, Parameter)

    def test_parameter_type(self):
        # Validates FIXED parameters
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                upper_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                values=(0, 2, 10, -1, 0, 7, 70, 9),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                upper_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
            )

        # Validates BOUNDED parameters
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                upper_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                values=(0, 2, 10, -1, 0, 7, 70, 9),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                values=(0, 2, 10, -1, 0, 7, 70, 9),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
            )

        # Validates length differences and emtpy tuples
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                upper_bounds=(0, 2, 10, -1, 0, 7, 70),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=tuple(),
                upper_bounds=tuple(),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=None,
                upper_bounds=None,
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                values=tuple(),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                values=None,
            )

        # Validates None values
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=None,
                value_type=ValueType.INTEGER,
                values=(0, 2, 10, -1, 0, 7, 70, 9),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=None,
                values=(0, 2, 10, -1, 0, 7, 70, 9),
            )

    def test_creation_with_binary_value_type(self):
        # Validate Fixed parameter set
        param_set1 = MultiValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.BINARY,
            values=(0, 1, 0, 1, 0, 1, 1),
        )

        assert param_set1 is not None
        assert not param_set1.is_bounded
        assert param_set1.value_type == ValueType.BINARY
        assert param_set1.parameter_type == ParameterType.FIXED
        assert param_set1.lower_bounds is None and param_set1.upper_bounds is None and param_set1.values is not None
        assert len(param_set1.values) == 7

        # Validate Bounded parameter set
        param_set2 = MultiValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.BINARY,
            lower_bounds=(0, 1, 0, 1, 0, 1, 1),
            upper_bounds=(1, 1, 1, 1, 0, 1, 1),
        )

        assert param_set2 is not None
        assert param_set2.is_bounded
        assert param_set2.value_type == ValueType.BINARY
        assert param_set2.parameter_type == ParameterType.BOUNDED
        assert param_set2.lower_bounds is not None and param_set2.upper_bounds is not None and param_set2.values is None
        assert len(param_set2.lower_bounds) == len(param_set2.upper_bounds) == 7

        # Validates integer numbers
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.BINARY,
                values=(0, 1, 0, 6, 0, 1, -1),
            )

        # Validates continuous numbers
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bounds=(0, 1, 0, 0, 0, 0, 1),
                upper_bounds=(0, 1, 0, 0, 0, 1.1, 1),
            )

        # Validates lower and upper bounds
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bounds=(0, 1, 0, 1, 0, 1, 1),
                upper_bounds=(1, 0, 1, 1, 0, 1, 1),
            )

    def test_creation_with_integer_value_type(self):
        # Validate Fixed parameter set
        param_set1 = MultiValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.INTEGER,
            values=(0, 2, 10, -1, 0, 7, 70, 9),
        )

        assert param_set1 is not None
        assert not param_set1.is_bounded
        assert param_set1.value_type == ValueType.INTEGER
        assert param_set1.parameter_type == ParameterType.FIXED
        assert param_set1.lower_bounds is None and param_set1.upper_bounds is None and param_set1.values is not None
        assert len(param_set1.values) == 8

        # Validate Bounded parameter set
        param_set2 = MultiValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.INTEGER,
            lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
            upper_bounds=(4, 5, 12, 0, 0, 8, 71, 50),
        )

        assert param_set2 is not None
        assert param_set2.is_bounded
        assert param_set2.value_type == ValueType.INTEGER
        assert param_set2.parameter_type == ParameterType.BOUNDED
        assert param_set2.lower_bounds is not None and param_set2.upper_bounds is not None and param_set2.values is None
        assert len(param_set2.lower_bounds) == len(param_set2.upper_bounds) == 8

        # Validates continuous numbers
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                values=(0, 2, 10, -1, 0.1, 7, 70, -9.5),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0.1, 7, 70, -9.5),
                upper_bounds=(0, 2, 10, -1, 1, 7, 70, 10),
            )

        # Validates lower and upper bounds
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bounds=(0, 2, 10, -1, 0, 7, 70, 9),
                upper_bounds=(4, 5, 12, -5, 0, 8, 71, 9),
            )

    def test_creation_with_continuous_value_type(self):
        # Validate Fixed parameter set
        param_set1 = MultiValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.CONTINUOUS,
            values=(0.1, 2.956, 10, -1.5, 0, 7, 70.2),
        )

        assert param_set1 is not None
        assert not param_set1.is_bounded
        assert param_set1.value_type == ValueType.CONTINUOUS
        assert param_set1.parameter_type == ParameterType.FIXED
        assert param_set1.lower_bounds is None and param_set1.upper_bounds is None and param_set1.values is not None
        assert len(param_set1.values) == 7

        # Validate Bounded parameter set
        param_set2 = MultiValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.CONTINUOUS,
            lower_bounds=(0.1, 2.956, 10, -1.5, 0, 7, 70.2),
            upper_bounds=(0.2, 2.958, 10, -1.2, 0, 7.5, 75),
        )

        assert param_set2 is not None
        assert param_set2.is_bounded
        assert param_set2.value_type == ValueType.CONTINUOUS
        assert param_set2.parameter_type == ParameterType.BOUNDED
        assert param_set2.lower_bounds is not None and param_set2.upper_bounds is not None and param_set2.values is None
        assert len(param_set2.lower_bounds) == len(param_set2.upper_bounds) == 7

        # Validates infinity
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.CONTINUOUS,
                values=(0.1, 2.956, 10, inf, 0, -inf, 70.2),
            )
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bounds=(0.1, 2.956, 10, 0, 0, -inf, 70.2),
                upper_bounds=(0.1, 2.956, 10, inf, 20, 0, 70.2),
            )

        # Validates lower and upper bounds
        with raises(ValueError):
            MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bounds=(0.1, 2.956, 10, -1.5, 0, 7, 75.00001),
                upper_bounds=(0.2, 2.958, 10, -1.7, 0, 7.5, 75),
            )
