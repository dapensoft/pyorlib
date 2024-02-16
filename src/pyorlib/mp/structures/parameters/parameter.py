from abc import ABC
from dataclasses import dataclass

from ...enums import ValueType, ParameterType


@dataclass(frozen=True)
class Parameter(ABC):
    """
    An abstract data class representing a parameter in an optimization model.

    The `Parameter` class is an abstract base class (ABC) that defines the common interface for parameters in an
    optimization model. It provides information about the type of the parameter and the value type of its values.
    """

    parameter_type: ParameterType
    """ The type of the parameter. """

    value_type: ValueType
    """ The value type of the parameter values. """

    @property
    def is_bounded(self) -> bool:
        """
        Returns a boolean indicating whether the parameter is bounded.
        :return: `True` if the parameter is bounded, `False` otherwise.
        """
        return self.parameter_type == ParameterType.BOUNDED
