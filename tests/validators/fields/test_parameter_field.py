from dataclasses import dataclass

from _pytest.python_api import raises

from pyorlib.enums import ParameterType, ValueType
from pyorlib.structures import SingleValueParameter, MultiValueParameter
from pyorlib.validators import ParameterField


class TestParameterField:

    def test_parameter_field_definition(self):

        @dataclass
        class ParameterSetSchema:
            param1: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.BOUNDED},
                value_types={ValueType.BINARY},
                min=1,
                max=7.5,
            )
            param2: MultiValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED},
                value_types={ValueType.CONTINUOUS},
                min=-5,
            )

        # Validates empty param types
        with raises(ValueError):

            @dataclass
            class ParameterSetSchema1:
                param1: SingleValueParameter = ParameterField(
                    parameter_types={},
                    value_types={ValueType.BINARY},
                )

        # Validates parameter_types None values
        with raises(ValueError):

            @dataclass
            class ParameterSetSchema2:
                param1: SingleValueParameter = ParameterField(
                    parameter_types=None,
                    value_types={ValueType.BINARY},
                )

        # Validates empty value types
        with raises(ValueError):

            @dataclass
            class ParameterSetSchema3:
                param1: SingleValueParameter = ParameterField(
                    parameter_types={ParameterType.BOUNDED},
                    value_types={},
                )

        # Validates value_types None values
        with raises(ValueError):

            @dataclass
            class ParameterSetSchema4:
                param1: SingleValueParameter = ParameterField(
                    parameter_types={ParameterType.BOUNDED},
                    value_types=None,
                )

        # Validates min and max values
        with raises(ValueError):

            @dataclass
            class ParameterSetSchema5:
                param1: SingleValueParameter = ParameterField(
                    parameter_types={ParameterType.BOUNDED},
                    value_types={ValueType.BINARY},
                    min=1.35,
                    max=-7.5,
                )

    def test_parameter_field_validations(self):
        @dataclass
        class ParameterSchema:
            param1: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED},
                value_types={ValueType.BINARY},
            )
            param2: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.BOUNDED},
                value_types={ValueType.INTEGER},
            )
            param3: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.CONTINUOUS},
                min=-3,
                max=100.01,
            )
            param4: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.CONTINUOUS},
                min=5,
                max=8,
            )
            param5: MultiValueParameter | None = ParameterField(
                parameter_types={ParameterType.FIXED},
                value_types={ValueType.BINARY},
                required=False,
            )
            param6: MultiValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.INTEGER, ValueType.CONTINUOUS},
                min=5.2,
                max=9.1,
            )

        # Validates descriptor properties
        assert (
            ParameterSchema.__dict__["param1"].parameter_types == {ParameterType.FIXED}
            and ParameterSchema.__dict__["param1"].value_types == {ValueType.BINARY}
            and ParameterSchema.__dict__["param1"].required
            and ParameterSchema.__dict__["param1"].min is None
            and ParameterSchema.__dict__["param1"].max is None
        )
        assert (
            ParameterSchema.__dict__["param2"].parameter_types == {ParameterType.BOUNDED}
            and ParameterSchema.__dict__["param2"].value_types == {ValueType.INTEGER}
            and ParameterSchema.__dict__["param2"].required
            and ParameterSchema.__dict__["param2"].min is None
            and ParameterSchema.__dict__["param2"].max is None
        )
        assert (
            ParameterSchema.__dict__["param3"].parameter_types == {ParameterType.FIXED, ParameterType.BOUNDED}
            and ParameterSchema.__dict__["param3"].value_types == {ValueType.CONTINUOUS}
            and ParameterSchema.__dict__["param3"].required
            and ParameterSchema.__dict__["param3"].min == -3
            and ParameterSchema.__dict__["param3"].max == 100.01
        )
        assert (
            ParameterSchema.__dict__["param4"].parameter_types == {ParameterType.FIXED, ParameterType.BOUNDED}
            and ParameterSchema.__dict__["param4"].value_types == {ValueType.CONTINUOUS}
            and ParameterSchema.__dict__["param4"].required
            and ParameterSchema.__dict__["param4"].min == 5
            and ParameterSchema.__dict__["param4"].max == 8
        )
        assert (
            ParameterSchema.__dict__["param5"].parameter_types == {ParameterType.FIXED}
            and ParameterSchema.__dict__["param5"].value_types == {ValueType.BINARY}
            and not ParameterSchema.__dict__["param5"].required
            and ParameterSchema.__dict__["param5"].min is None
            and ParameterSchema.__dict__["param5"].max is None
        )
        assert (
            ParameterSchema.__dict__["param6"].parameter_types == {ParameterType.FIXED, ParameterType.BOUNDED}
            and ParameterSchema.__dict__["param6"].value_types == {ValueType.INTEGER, ValueType.CONTINUOUS}
            and ParameterSchema.__dict__["param6"].required
            and ParameterSchema.__dict__["param6"].min == 5.2
            and ParameterSchema.__dict__["param6"].max == 9.1
        )

        # Validates creation
        param1 = SingleValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.BINARY,
            value=1,
        )
        param2 = SingleValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.INTEGER,
            lower_bound=2,
            upper_bound=3,
        )
        param3 = SingleValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.CONTINUOUS,
            value=-1.1,
        )
        param4 = SingleValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.CONTINUOUS,
            lower_bound=5.4,
            upper_bound=5.5,
        )
        param6 = MultiValueParameter(
            parameter_type=ParameterType.BOUNDED,
            value_type=ValueType.CONTINUOUS,
            lower_bounds=(5.2, 5.3, 5.4),
            upper_bounds=(8.6, 9.0, 9.1),
        )
        param7 = MultiValueParameter(
            parameter_type=ParameterType.FIXED,
            value_type=ValueType.INTEGER,
            values=(6, 7, 8),
        )
        params = ParameterSchema(param1=param1, param2=param2, param3=param3, param4=param4, param5=None, param6=param6)
        assert params is not None

        # Validates the assignment of multiple param types
        params.param6 = param7
        assert params.param6 == param7

        params.param6 = param6
        assert params.param6 == param6

        # Validates supported param types (FIXED only)
        with raises(ValueError):
            params.param1 = SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.BINARY,
                lower_bound=0,
                upper_bound=1,
            )
        assert params.param1 == param1

        # Validates supported param types (BOUNDED only)
        with raises(ValueError):
            params.param2 = SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                value=3,
            )
        assert params.param2 == param2

        # Validates supported value types
        with raises(ValueError):
            params.param2 = SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bound=2,
                upper_bound=3,
            )
        assert params.param2 == param2

        # Validates required params
        with raises(ValueError):
            params.param3 = None
        assert params.param3 == param3

        # Validates param3 min value with -4
        with raises(ValueError):
            params.param3 = SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.CONTINUOUS,
                value=-3.1,
            )
        assert params.param3 == param3

        # Validates param4 min value with 4.9
        with raises(ValueError):
            params.param4 = SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bound=4.9,
                upper_bound=5.5,
            )
        assert params.param4 == param4

        # Validates param6 min value with 5.1 in the first lb value
        with raises(ValueError):
            params.param6 = MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bounds=(5.1, 5.3, 5.4),
                upper_bounds=(8.6, 9.0, 9.1),
            )
        assert params.param6 == param6

        # Validates param6 min value with 5 in the first lb value (FIXED, INTEGER)
        with raises(ValueError):
            params.param6 = MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                values=(5, 7, 8),
            )
        assert params.param6 == param6

        # Validates param3 max value with 100.1
        with raises(ValueError):
            params.param3 = SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.CONTINUOUS,
                value=100.1,
            )
        assert params.param3 == param3

        # Validates param4 max value with 8.1
        with raises(ValueError):
            params.param4 = SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bound=5.0,
                upper_bound=8.1,
            )
        assert params.param4 == param4

        # Validates param6 max value with 9.2 in the last ub value
        with raises(ValueError):
            params.param6 = MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bounds=(5.2, 5.3, 5.4),
                upper_bounds=(8.6, 9.0, 9.2),
            )
        assert params.param6 == param6

        # Validates param6 max value with 10 in the last ub value (FIXED, INTEGER)
        with raises(ValueError):
            params.param6 = MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.INTEGER,
                values=(6, 7, 10),
            )
        assert params.param6 == param6
