from ...core.validators.fields import FieldValidator
from ...validators.value_type_validator import ValueTypeValidator


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
    def min(self) -> int | None:
        """
        Get the minimum value allowed.
        :return: The minimum value or None if not set.
        """
        return self._min

    @property
    def max(self) -> int | None:
        """
        Get the maximum value allowed.
        :return: The maximum value or None if not set.
        """
        return self._max

    def __init__(self, min: int | None = None, max: int | None = None):
        """
        Initialize a new DimensionField instance.
        :param min: The minimum value allowed for the dimension field. Defaults to None.
        :param max: The maximum value allowed for the dimension field. Defaults to None.
        """
        # Calls the base init method
        super().__init__()

        # Applies validations
        if min is not None and not ValueTypeValidator.is_integer(min):
            raise ValueError(f"{self._public_name} 'min' value must be an integer number.")

        if max is not None and not ValueTypeValidator.is_integer(max):
            raise ValueError(f"{self._public_name} 'max' value must be an integer number.")

        if min is not None and min < 0:
            raise ValueError(f"{self._public_name} 'min' value must be greater than or equal to 0.")

        if max is not None and min is not None and min > max:
            raise ValueError(f"{self._public_name} 'min' value cannot be greater than maximum.")

        # Instance attributes
        self._min: int | None = min
        self._max: int | None = max

    def validate(self, value: int | None) -> None:
        if value is None:
            raise ValueError(f"{self._public_name} value cannot be None.")

        if not ValueTypeValidator.is_integer(value):
            raise ValueError(f"{self._public_name} value must be an integer number.")

        if self._min is not None and value < self._min:
            raise ValueError(f"{self._public_name} value must be greater than or equal to {self._min}.")

        if self._max is not None and value > self._max:
            raise ValueError(f"{self._public_name} value must be less than or equal to {self._max}.")
