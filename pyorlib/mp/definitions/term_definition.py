from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class TermDefinition:
    """ A dataclass for defining the specifications of a term in a model. """

    name: Callable[..., str] | str
    """ 
    The name of the term. It could be a callable that returns the indexed name 
    of the term (eg (1, 2) -> 'x_1_2') or a string with the name itself.
    """

    set_name: str | None = None
    """ The name of the term set to which this term belongs. """

    display_name: str | None = None
    """ The name of the term as it should be displayed to the user. """
