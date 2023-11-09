from dataclasses import dataclass

from _pytest.python_api import raises

from pyorlib.mp.common.enums import ParameterType, ValueType
from pyorlib.mp.input.descriptors import ParameterField
from pyorlib.mp.input.parameters import SingleValueParameter, MultiValueParameter


class TestParameterField:

    def test_parameter_field_validation(self):
        @dataclass
        class ParameterSchema:
            param1: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED},
                value_types={ValueType.BINARY}
            )
            param2: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.BOUNDED},
                value_types={ValueType.INTEGER}
            )
            param3: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.CONTINUOUS}
            )
            param4: SingleValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.CONTINUOUS},
                min=5,
                max=8,
            )
            param5: SingleValueParameter | None = ParameterField(
                parameter_types={ParameterType.FIXED},
                value_types={ValueType.CONTINUOUS},
                required=False,
            )

        ParameterSchema(
            param1=SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.BINARY,
                value=1
            ),
            param2=SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.INTEGER,
                lower_bound=2, upper_bound=3,
            ),
            param3=SingleValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.CONTINUOUS,
                value=-1.1
            ),
            param4=SingleValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bound=5.4, upper_bound=5.5,
            ),
            param5=None
        )

        # Validates supported param types
        with raises(Exception):
            ParameterSchema(
                param1=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.BINARY,
                    value=1
                ),
                param2=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.INTEGER,
                    lower_bound=2, upper_bound=3,
                ),
                param3=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.CONTINUOUS,
                    value=-1.1
                ),
                param4=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.CONTINUOUS,
                    lower_bound=5.4, upper_bound=5.5,
                ),
                param5=None
            )

        # Validates supported value types
        with raises(Exception):
            ParameterSchema(
                param1=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.CONTINUOUS,
                    value=1
                ),
                param2=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.INTEGER,
                    lower_bound=2, upper_bound=3,
                ),
                param3=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.CONTINUOUS,
                    value=-1.1
                ),
                param4=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.CONTINUOUS,
                    lower_bound=5.4, upper_bound=5.5,
                ),
                param5=None
            )

        # Validates required params
        with raises(Exception):
            ParameterSchema(
                param1=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.BINARY,
                    value=1
                ),
                param2=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.INTEGER,
                    lower_bound=2, upper_bound=3,
                ),
                param3=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.CONTINUOUS,
                    value=-1.1
                ),
                param4=None,
                param5=None
            )

        # Validates min and max
        with raises(Exception):
            ParameterSchema(
                param1=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.BINARY,
                    value=1
                ),
                param2=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.INTEGER,
                    lower_bound=2, upper_bound=3,
                ),
                param3=SingleValueParameter(
                    parameter_type=ParameterType.FIXED,
                    value_type=ValueType.CONTINUOUS,
                    value=-1.1
                ),
                param4=SingleValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.CONTINUOUS,
                    lower_bound=2.5, upper_bound=9,
                ),
                param5=None
            )

    def test_parameter_field_validation_with_parameter_sets(self):
        @dataclass
        class ParameterSetSchema:
            param1: MultiValueParameter = ParameterField(
                parameter_types={ParameterType.FIXED, ParameterType.BOUNDED},
                value_types={ValueType.CONTINUOUS},
                min=5.2,
                max=8.5,
            )

        ParameterSetSchema(
            param1=MultiValueParameter(
                parameter_type=ParameterType.BOUNDED,
                value_type=ValueType.CONTINUOUS,
                lower_bounds=(5.2, 5.3, 5.4),
                upper_bounds=(8.5, 8.4, 8.3),
            ),
        )

        ParameterSetSchema(
            param1=MultiValueParameter(
                parameter_type=ParameterType.FIXED,
                value_type=ValueType.CONTINUOUS,
                values=(5.2, 5.3, 5.4),
            ),
        )

        # Validates min
        with raises(Exception):
            ParameterSetSchema(
                param1=MultiValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.CONTINUOUS,
                    lower_bounds=(5.1, 5.3, 5.4),
                    upper_bounds=(8.5, 8.4, 8.3),
                ),
            )

        # Validates max
        with raises(Exception):
            ParameterSetSchema(
                param1=MultiValueParameter(
                    parameter_type=ParameterType.BOUNDED,
                    value_type=ValueType.CONTINUOUS,
                    lower_bounds=(5.2, 5.3, 5.4),
                    upper_bounds=(8.6, 8.4, 8.3),
                ),
            )

    def test_invalid_parameter_field_definition(self):
        # Validates empty param types
        with raises(Exception):
            @dataclass
            class InvalidParameterSetSchema1:
                param1: MultiValueParameter = ParameterField(
                    parameter_types={},
                    value_types={ValueType.CONTINUOUS},
                    min=5.2,
                    max=8.5,
                )

        # Validates empty value types
        with raises(Exception):
            @dataclass
            class InvalidParameterSetSchema1:
                param1: MultiValueParameter = ParameterField(
                    parameter_types={ParameterType.FIXED},
                    value_types={},
                    min=5.2,
                    max=8.5,
                )

        # Validates invalid min and max values
        with raises(Exception):
            @dataclass
            class InvalidParameterSetSchema1:
                param1: MultiValueParameter = ParameterField(
                    parameter_types={ParameterType.FIXED},
                    value_types={ValueType.CONTINUOUS},
                    min=8.6,
                    max=8.5,
                )
