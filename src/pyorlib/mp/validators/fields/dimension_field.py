from src.pyorlib.core.validators.fields import FieldValidator
from src.pyorlib.mp.validators.value_type_validator import ValueTypeValidator


class DimensionField(FieldValidator[int]):
    """
    A descriptor used to validate dimensions in an optimization model.

    The `DimensionField` class is a field validator specifically designed for model's dimension fields. It ensures that
    the dimension value is within specified bounds and is an integer number. It allows setting minimum and maximum
    limits for the dimension.

    This class is a subclass of `FieldValidator` and inherits its functionality for validating and formatting field
    values.
    """

    __slots__ = ["_min", "_max"]

    @property
    def min(self) -> float | None:
        """
        Get the minimum value allowed.
        :return: The minimum value or None if not set.
        """
        return self._min

    @property
    def max(self) -> float | None:
        """
        Get the maximum value allowed.
        :return: The maximum value or None if not set.
        """
        return self._max

    def __init__(self, min: float | None = None, max: float | None = None):
        """
        Initialize a new DimensionField instance.
        :param min: The minimum value allowed for the dimension field. Defaults to None.
        :param max: The maximum value allowed for the dimension field. Defaults to None.
        """
        super().__init__()
        self._min: float | None = min
        self._max: float | None = max

        # Validations
        if self.min is not None and self.min < 1:
            raise ValueError("Dimension field minimum must be greater than or equal to 1.")

        if self.max is not None and self.min is not None and self.min > self.max:
            raise ValueError("Dimension field minimum cannot be greater than maximum.")

    def validate(self, value: int | None):
        if value is None:
            raise ValueError(f"{self._public_name} cannot be None")

        if self._min is not None and value < self._min:
            raise ValueError(f"{self._public_name} value must be greater than or equal to {self._min}")

        if self._max is not None and value > self._max:
            raise ValueError(f"{self._public_name} value must be less than or equal to {self._max}")

        if not ValueTypeValidator.is_integer(value):
            raise ValueError(f"{self._public_name} value must be a valid integer number")
