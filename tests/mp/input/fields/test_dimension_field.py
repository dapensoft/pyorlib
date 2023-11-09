from dataclasses import dataclass

from _pytest.python_api import raises

from pyorlib.mp.input.descriptors import DimensionField


class TestDimensionField:

    def test_dimension_field_validation(self):
        @dataclass
        class DimensionSchema:
            r: int = DimensionField()
            s: int = DimensionField(min=2)
            d: int = DimensionField(max=8)
            t: int = DimensionField(min=3, max=3)

        DimensionSchema(r=2, s=4, t=3, d=5)

        # Validates min value
        with raises(Exception):
            DimensionSchema(r=2, s=1, t=3, d=5)

        # Validates max value
        with raises(Exception):
            DimensionSchema(r=2, s=4, t=3, d=9)

        # Validates min and max value
        with raises(Exception):
            DimensionSchema(r=2, s=4, t=2, d=5)

        # Validates non integer values
        with raises(Exception):
            DimensionSchema(r=2.2, s=4, t=3, d=5)

    def test_invalid_dimension_field_definition(self):
        # Validates min value
        with raises(Exception):
            @dataclass
            class InvalidDimensionSchema:
                s: int = DimensionField(min=2, max=0)
