from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class TermDefinition:
    """
    Represents the definition of a term in an optimization model.

    It provides a way to define the characteristics of a Term, such as its name,
    the term set it belongs to (if applicable), and the display name for the term.
    """

    name: Callable[..., str] | str
    """ 
    The name of the term. It can be a callable that returns the indexed name
    of the term (e.g., `lambda` i, j: 'x_i_j'), or a string with the name itself.
    """

    set_name: str | None = None
    """ The name of the term set to which this term belongs (e.g., x_i_j). """

    display_name: str | None = None
    """ The name of the term as it should be displayed to the user. """
