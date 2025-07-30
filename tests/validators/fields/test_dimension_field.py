from dataclasses import dataclass

from pytest import raises

from pyorlib.validators import DimensionField


class TestDimensionField:

    def test_dimension_field_definition(self):

        @dataclass
        class DimensionSchema:
            s: int = DimensionField()

        # Validates non integer min value
        with raises(Exception):

            @dataclass
            class DimensionSchema1:
                s: int = DimensionField(min=0.1)

        # Validates non integer max value
        with raises(Exception):

            @dataclass
            class DimensionSchema2:
                s: int = DimensionField(max=5.6)

        # Validates invalid min value
        with raises(Exception):

            @dataclass
            class DimensionSchema3:
                s: int = DimensionField(min=-1)

        # Validates invalid min/max values
        with raises(Exception):

            @dataclass
            class DimensionSchema4:
                s: int = DimensionField(min=2, max=1)

    def test_dimension_field_validation(self):
        @dataclass
        class DimensionSchema:
            r: int = DimensionField()
            s: int = DimensionField(min=2)
            t: int = DimensionField(min=3, max=3)
            d: int = DimensionField(max=8)

        # Validates descriptor properties
        assert DimensionSchema.__dict__["r"].min is None and DimensionSchema.__dict__["r"].max is None
        assert DimensionSchema.__dict__["s"].min == 2 and DimensionSchema.__dict__["s"].max is None
        assert DimensionSchema.__dict__["t"].min == 3 and DimensionSchema.__dict__["t"].max == 3
        assert DimensionSchema.__dict__["d"].min is None and DimensionSchema.__dict__["d"].max == 8

        # Validates creation
        dim = DimensionSchema(r=2, s=4, t=3, d=5)
        assert dim is not None

        # Validates non integer values
        with raises(Exception):
            dim.r = 2.2
        assert dim.r == 2

        # Validates min value
        with raises(Exception):
            dim.s = 1
        assert dim.s == 4

        # Validates None values
        with raises(Exception):
            dim.t = None
        assert dim.t == 3

        # Validates max value
        with raises(Exception):
            dim.d = 9
        assert dim.d == 5
