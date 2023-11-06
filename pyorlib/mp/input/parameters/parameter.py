from abc import ABC
from dataclasses import dataclass

from pyorlib.mp.common.enums import ValueType, ParameterType


@dataclass(frozen=True)
class Parameter(ABC):
    """ An abstract dataclass for a model parameter. """

    parameter_type: ParameterType
    """ The type of the parameter. """

    value_type: ValueType
    """ The ValueType of the parameter value. """

    @property
    def is_bounded(self) -> bool:
        """
        Returns a boolean indicating whether the parameter is bounded.
        :return: A boolean indicating whether the parameter is bounded.
        """
        return self.parameter_type == ParameterType.BOUNDED
