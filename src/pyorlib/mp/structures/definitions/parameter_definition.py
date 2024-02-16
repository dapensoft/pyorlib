from dataclasses import dataclass
from typing import Set, Callable

from ...enums import ValueType, ParameterType


@dataclass(frozen=True)
class ParameterDefinition:
    """
    Represents the definition of a parameter in an optimization model.

    It provides various attributes to define the characteristics of the parameter in an optimization problem.
    """

    name: Callable[..., str] | str
    """ 
    The name of the parameter. It can be a callable that returns the indexed name
    of the parameter (e.g., `lambda` i, j: 'c_i_j'), or a string with the name itself.
    """

    parameter_types: Set[ParameterType]
    """ A set of parameter types supported by the parameter. """

    value_types: Set[ValueType]
    """ A set of value types supported by the parameter. """

    set_name: str | None = None
    """ The name of the term set to which this parameter belongs (e.g., c_i_j). """

    display_name: str | None = None
    """ The name of the parameter as it should be displayed to the user. """

    min: float | int | None = None
    """ The minimum value allowed for the parameter. """

    max: float | int | None = None
    """ The maximum value allowed for the parameter. """
