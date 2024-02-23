from typing import Set

from ...core.validators.fields import FieldValidator
from ...enums import ParameterType, ValueType
from ...structures.parameters import MultiValueParameter, SingleValueParameter
from ...structures.parameters import Parameter


class ParameterField(FieldValidator[Parameter]):
    """
    A descriptor used to validate parameters in an optimization model.

    The `ParameterField` class is designed specifically for validating parameters in an optimization model. It ensures
    that the parameter value is of the correct type and format and provides functionality for validating and formatting
    parameter values based on defined constraints and requirements.

    This class is a subclass of `FieldValidator` and inherits its functionality for validating and formatting field
    values.
    """

    __slots__ = [
        "_required",
        "_parameter_types",
        "_value_types",
        "_min",
        "_max",
    ]

    @property
    def parameter_types(self) -> Set[ParameterType]:
        """
        Returns the set of supported parameter types.
        :return: A set containing the supported parameter types.
        """
        return self._parameter_types

    @property
    def value_types(self) -> Set[ValueType]:
        """
        Returns the set of supported value types.
        :return: A set containing the supported value types.
        """
        return self._value_types

    @property
    def min(self) -> float | None:
        """
        Returns the minimum supported value of the descriptor.
        :return: The minimum supported value. If there is no minimum value, it is None.
        """
        return self._min

    @property
    def max(self) -> float | None:
        """
        Returns the maximum supported value of the descriptor.
        :return: The maximum supported value. If there is no maximum value, it is None.
        """
        return self._max

    @property
    def required(self) -> bool:
        """
        Returns a boolean indicating whether the parameter is required.
        :return: `True` if the parameter is required, `False` otherwise.
        """
        return self._required

    def __init__(
        self,
        parameter_types: Set[ParameterType],
        value_types: Set[ValueType],
        min: float | None = None,
        max: float | None = None,
        required: bool = True,
    ):
        """
        Initialize a new instance of ParameterField.
        :param parameter_types: A set that contains the supported parameter types.
        :param value_types: A set that contains the supported value types.
        :param min: The minimum value supported by the descriptor. If there is no minimum value, it is None.
        :param max: The maximum value supported by the descriptor. If there is no maximum value, it is None.
        :param required: A boolean indicating whether the parameter is required or not.
        """
        # Calls the base init method
        super().__init__()

        # Applies validations
        if parameter_types is None or len(parameter_types) == 0:
            raise ValueError("The set of parameter types cannot be empty.")

        if value_types is None or len(value_types) == 0:
            raise ValueError("The set of value types cannot be empty.")

        if max is not None and min is not None and min > max:
            raise ValueError("The minimum value for the parameter field cannot be greater than the maximum value.")

        self._parameter_types: Set[ParameterType] = parameter_types
        """ A set of parameter types that are supported by the descriptor. """

        self._value_types: Set[ValueType] = value_types
        """ A set of value types that are supported by the descriptor. """

        self._min: float | None = min
        """ The minimum value supported by the descriptor, or None if there is no minimum value. """

        self._max: float | None = max
        """ The maximum value supported by the descriptor, or None if there is no maximum value. """

        self._required: bool = required
        """ A boolean indicating whether the parameter is required. """

    def validate(self, value: Parameter | None) -> None:
        # Checks for None value
        if value is None:
            if self.required:
                raise ValueError(f"{self._public_name} is required")
            else:
                return

        # Checks for supported param types
        if not value.is_bounded and ParameterType.FIXED not in self.parameter_types:
            raise ValueError(f"{self._public_name} does not support {ParameterType.FIXED.name}")
        if value.is_bounded and ParameterType.BOUNDED not in self.parameter_types:
            raise ValueError(f"{self._public_name} does not support {ParameterType.BOUNDED.name}")

        # Checks for supported value types
        if value.value_type not in self.value_types:
            raise ValueError(f"{self._public_name} does not support {value.value_type.name}")

        # Checks for SingleValueParameter and MultiValueParameter types
        if isinstance(value, MultiValueParameter):
            if value.is_bounded:
                if self._min is not None or self._max is not None:
                    for i in range(0, len(value.lower_bounds)):  # type: ignore[arg-type]
                        lb = value.lower_bounds[i]  # type: ignore[index]
                        ub = value.upper_bounds[i]  # type: ignore[index]
                        self._validate_bounds(lb, ub)
            else:
                if self._min is not None or self._max is not None:
                    for val in value.values:  # type: ignore[union-attr]
                        self._validate_value(val)
        elif isinstance(value, SingleValueParameter):
            if value.is_bounded:
                if self._min is not None or self._max is not None:
                    self._validate_bounds(value.lower_bound, value.upper_bound)  # type: ignore[arg-type]
            else:
                if self._min is not None or self._max is not None:
                    self._validate_value(value.value)  # type: ignore[arg-type]
        else:
            raise TypeError(f"{self._public_name} invalid parameter type")  # pragma: no cover

    def _validate_bounds(self, lower_bound: float, upper_bound: float) -> None:
        """
        Validates the specified bounds for the parameter value.
        :param lower_bound: The lower bound of the parameter.
        :param upper_bound: The upper bound of the parameter.
        :return: None
        """
        if self._min is not None and lower_bound < self._min:
            raise ValueError(f"{self._public_name} lower bound must be greater than or equal to {self._min}")
        if self._max is not None and upper_bound > self._max:
            raise ValueError(f"{self._public_name} upper bound must be less than or equal to {self._max}")

    def _validate_value(self, value: float) -> None:
        """
        Validates a given parameter value.
        :param value: The parameter value to be validated.
        :return: None
        """
        if self._min is not None and value < self._min:
            raise ValueError(f"{self._public_name} value must be greater than or equal to {self._min}")
        if self._max is not None and value > self._max:
            raise ValueError(f"{self._public_name} value must be less than or equal to {self._max}")
