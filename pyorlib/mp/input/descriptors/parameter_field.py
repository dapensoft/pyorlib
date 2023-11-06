from typing import Set

from pyorlib.core.descriptors import FieldValidator
from pyorlib.mp.common.enums import ParameterType, ValueType
from pyorlib.mp.input.parameters import Parameter
from pyorlib.mp.input.parameters.multi import MultiValueParameter
from pyorlib.mp.input.parameters.single import SingleValueParameter


class ParameterField(FieldValidator[Parameter]):
    """ A descriptor for validating model parameters.  """

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
        Returns a set of parameter types that are supported by the descriptor.
        :return: A set of parameter types that are supported by the descriptor.
        """
        return self._parameter_types

    @property
    def value_types(self) -> Set[ValueType]:
        """
        Returns a set of value types that are supported by the descriptor.
        :return: A set of value types that are supported by the descriptor.
        """
        return self._value_types

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

    @property
    def required(self) -> bool:
        """
        Returns a boolean indicating whether the parameter is required.
        :return: True if the parameter is required, False otherwise.
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
        Instantiate a new ParameterField descriptor.
        :param parameter_types: A set of ParameterType representing the types of parameters that are supported.
        :param value_types: A set of ValueType representing the types of values that are supported.
        :param min: An optional parameter specifying the minimum value that is supported.
        :param max: An optional parameter specifying the maximum value that is supported.
        :param required: A boolean indicating whether the parameter is required.
        """

        super().__init__()
        self._parameter_types: Set[ParameterType] = parameter_types
        self._value_types: Set[ValueType] = value_types
        self._min: float | None = min
        self._max: float | None = max
        self._required: bool = required

        # Validations
        if len(self.parameter_types) == 0:
            raise ValueError("Parameter field parameter types cannot be emtpy")

        if len(self.value_types) == 0:
            raise ValueError("Parameter field value types cannot be emtpy")

        if self.min is not None and self.min < 0:
            raise ValueError("Parameter field minimum must be greater than or equal to 0")

        if self.max is not None and self.min is not None and self.min > self.max:
            raise ValueError("Parameter field minimum cannot be greater than maximum")

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
                    for i in range(0, len(value.lower_bounds)):
                        lb = value.lower_bounds[i]
                        ub = value.upper_bounds[i]
                        self._validate_bounds(lb, ub)
            else:
                if self._min is not None or self._max is not None:
                    for val in value.values:
                        self._validate_value(val)
        elif isinstance(value, SingleValueParameter):
            if value.is_bounded:
                if self._min is not None or self._max is not None:
                    self._validate_bounds(value.lower_bound, value.upper_bound)
            else:
                if self._min is not None or self._max is not None:
                    self._validate_value(value.value)
        else:
            raise TypeError(f"{self._public_name} invalid parameter type")

    def _validate_bounds(self, lower_bound: float, upper_bound: float) -> None:
        """
        Validates the specified bounds for the parameter value.
        :param lower_bound: The lower bound of the parameter value.
        :param upper_bound: The upper bound of the parameter value.
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
