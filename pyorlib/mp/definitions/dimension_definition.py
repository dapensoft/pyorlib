from dataclasses import dataclass


@dataclass(frozen=True)
class DimensionDefinition:
    """ A dataclass for defining the specification of a dimension in a model. """

    name: str
    """ The name of the dimension. """

    display_name: str | None = None
    """ The name of the dimension as it should be displayed to the user. """

    min: float | int | None = 1
    """ The minimum value that the dimension can take on. """

    max: float | int | None = None
    """ The maximum value that the dimension can take on. """
