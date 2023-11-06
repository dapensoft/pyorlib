from dataclasses import dataclass
from typing import Set, Callable

from pyorlib.mp.common.enums import ValueType, ParameterType


@dataclass(frozen=True)
class ParameterDefinition:
    """ A dataclass for defining the specification of a parameter in a model. """

    name: Callable[..., str] | str
    """ 
    The name of the parameter. It could be a callable that returns the indexed name 
    of the parameter (eg (1, 2) -> 'c_1_2') or a string with the name itself.
    """

    parameter_types: Set[ParameterType]
    """ A set of parameter types that are supported by the parameter. """

    value_types: Set[ValueType]
    """ A set of value types that are supported by the parameter. """

    set_name: str | None = None
    """ The name of the term set to which this parameter belongs. """

    display_name: str | None = None
    """ The name of the parameter as it should be displayed to the user. """

    min: float | int | None = None
    """ The minimum value that the parameter can take on. """

    max: float | int | None = None
    """ The maximum value that the parameter can take on. """
