from dataclasses import dataclass


@dataclass(frozen=True)
class DimensionDefinition:
    """
    Represents the definition of a dimension in an optimization model.

    It provides a way to define the characteristics of a dimension, such as its name, display name,
    minimum and maximum values allowed.
    """

    name: str
    """ The name of the dimension. """

    display_name: str | None = None
    """ The name of the dimension as it should be displayed to the user. """

    min: float | int | None = 1
    """ The minimum value allowed for the dimension. """

    max: float | int | None = None
    """ The maximum value allowed for the dimension. """
