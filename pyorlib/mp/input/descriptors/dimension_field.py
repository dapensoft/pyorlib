from pyorlib.core.descriptors import FieldValidator
from pyorlib.mp.common.validators import ValueTypeValidator


class DimensionField(FieldValidator[int]):
    """ A descriptor for validating model dimensions. """

    __slots__ = ["_min", "_max"]

    @property
    def min(self) -> float | None:
        """
        Returns the minimum value that is supported by the descriptor, or None if there is no minimum value.
        :return: The minimum value supported by the descriptor, or None if there is no minimum value.
        """
        return self._min

    @property
    def max(self) -> float | None:
        """
        Returns the maximum value that is supported by the descriptor, or None if there is no maximum value.
        :return: The maximum value supported by the descriptor, or None if there is no maximum value.
        """
        return self._max

    def __init__(self, min: float | None = None, max: float | None = None):
        """
        Instantiate a new DimensionField descriptor.
        :param min: An optional parameter specifying the minimum value that is supported.
        :param max: An optional parameter specifying the maximum value that is supported.
        """
        super().__init__()
        self._min: float | None = min
        self._max: float | None = max

        # Validations
        if self.min is not None and self.min < 1:
            raise ValueError("Dimension field minimum must be greater than or equal to 1")

        if self.max is not None and self.min is not None and self.min > self.max:
            raise ValueError("Dimension field minimum cannot be greater than maximum")

    def validate(self, value: int | None):
        if value is None:
            raise ValueError(f"{self._public_name} cannot be None")

        if self._min is not None and value < self._min:
            raise ValueError(f"{self._public_name} value must be greater than or equal to {self._min}")

        if self._max is not None and value > self._max:
            raise ValueError(f"{self._public_name} value must be less than or equal to {self._max}")

        if not ValueTypeValidator.is_integer(value):
            raise ValueError(f"{self._public_name} value must be a valid integer number")
