from dataclasses import dataclass

from .parameter import Parameter
from ...enums import ParameterType, ValueType
from ...validators import ValueTypeValidator


@dataclass(frozen=True)
class SingleValueParameter(Parameter):
    """
    A data class representing a single-value parameter in an optimization model.

    The `SingleValueParameter` class is a subclass of `Parameter` and is used to represent parameters with a single
    value in an optimization model. It provides properties to access the parameter value, lower bound, and upper bound.
    """

    value: float | None = None
    """ The value of the parameter, or None if no value is specified. """

    lower_bound: float | None = None
    """ The lower bound of the parameter, or None if no lower bound is specified. """

    upper_bound: float | None = None
    """ The upper bound of the parameter, or None if no upper bound is specified. """

    def __post_init__(self) -> None:
        # Parameter Validations
        if self.value_type is None:
            raise ValueError("Parameter value type is required.")

        if self.parameter_type == ParameterType.FIXED and self.value is not None:
            if self.lower_bound is not None or self.upper_bound is not None:
                raise ValueError("Parameters with value cannot has bounds.")
            if self.value >= 1e20 or self.value <= -1e20:
                raise ValueError("Parameter value cannot be infinity.")

            # Validate value and value type
            if self.value_type == ValueType.BINARY and not ValueTypeValidator.is_binary(self.value):
                raise ValueError("Parameter value must be a valid binary number.")
            elif self.value_type == ValueType.INTEGER and not ValueTypeValidator.is_integer(self.value):
                raise ValueError("Parameter value must be a valid integer number.")
        elif (
            self.parameter_type == ParameterType.BOUNDED
            and self.lower_bound is not None
            and self.upper_bound is not None
        ):
            if self.value is not None:
                raise ValueError("Parameters with bounds cannot has a value.")
            if self.upper_bound >= 1e20 or self.lower_bound <= -1e20:
                raise ValueError("Parameter upper bound cannot be infinity.")
            if self.lower_bound > self.upper_bound:
                raise ValueError("The upper bound of the parameter must be greater than or equal to the lower bound.")

            # Validate lower and upper bound values and value type
            if self.value_type == ValueType.BINARY and (
                not ValueTypeValidator.is_binary(self.lower_bound) or not ValueTypeValidator.is_binary(self.upper_bound)
            ):
                raise ValueError("Parameter lower and upper bound values must be valid binary numbers.")
            elif self.value_type == ValueType.INTEGER and (
                not ValueTypeValidator.is_integer(self.lower_bound)
                or not ValueTypeValidator.is_integer(self.upper_bound)
            ):
                raise ValueError("Parameter lower and upper bound values must be valid integer numbers.")
        else:
            raise ValueError("Invalid parameter.")
