from dataclasses import dataclass
from typing import Tuple

from pyorlib.mp.common.enums import ParameterType, ValueType
from pyorlib.mp.common.validators import ValueTypeValidator
from pyorlib.mp.input.parameters.parameter import Parameter


@dataclass(frozen=True)
class MultiValueParameterSet(Parameter):
    """ A data class for a multi value parameter in a model. """

    values: Tuple[float, ...] | None = None
    """ A set of parameter values. """

    lower_bounds: Tuple[float, ...] | None = None
    """ A set of parameter lower bounds. """

    upper_bounds: Tuple[float, ...] | None = None
    """ A set of parameter upper bounds. """

    def __post_init__(self):
        # Parameter Validations
        if self.value_type is None:
            raise ValueError("Parameter value type is required")

        if self.parameter_type == ParameterType.FIXED and self.values is not None:
            if self.lower_bounds is not None or self.upper_bounds is not None:
                raise ValueError("Parameters with values cannot have bounds")
            if len(self.values) == 0:
                raise ValueError("Parameters values cannot be empty")
            for val in self.values:
                if val >= 1e20 or val <= -1e20:
                    raise ValueError("Parameter values cannot be (+/-)infinity")

                # Value and Value Type validations
                if self.value_type == ValueType.BINARY and not ValueTypeValidator.is_binary(val):
                    raise ValueError("Parameter set values must be valid binary numbers")
                elif self.value_type == ValueType.INTEGER and not ValueTypeValidator.is_integer(val):
                    raise ValueError("Parameter set values must be valid integer numbers")
        elif (self.parameter_type == ParameterType.BOUNDED and
              self.lower_bounds is not None and
              self.upper_bounds is not None):
            if self.values is not None:
                raise ValueError("Parameters with bounds cannot have a value")
            if len(self.lower_bounds) != len(self.upper_bounds):
                raise ValueError("Parameters bounds must have the same length")
            if len(self.lower_bounds) == 0:
                raise ValueError("Parameters bounds cannot be empty")
            for i in range(0, len(self.lower_bounds)):
                lb = self.lower_bounds[i]
                ub = self.upper_bounds[i]
                if lb > ub:
                    raise ValueError("Parameters lower bounds cannot be greater than upper bounds")

                if ub >= 1e20 or lb < -1e20:
                    raise ValueError("Parameter upper and lower bounds cannot be (+/-)infinity")

                # lb and ub values and value type validation
                if (self.value_type == ValueType.BINARY and (
                        not ValueTypeValidator.is_binary(lb) or
                        not ValueTypeValidator.is_binary(ub))):
                    raise ValueError("Parameter lower and upper bound values must be valid binary numbers")
                elif (self.value_type == ValueType.INTEGER and (
                        not ValueTypeValidator.is_integer(lb) or
                        not ValueTypeValidator.is_integer(ub))):
                    raise ValueError("Parameter lower and upper bound values must be valid integer numbers")
        else:
            raise ValueError("Invalid parameter")
