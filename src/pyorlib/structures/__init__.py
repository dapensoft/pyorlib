"""
The Structures module in PyORlib provides a set of classes for managing and manipulating various structures encountered
in optimization modeling.
"""

from .definitions import DimensionDefinition, ParameterDefinition, TermDefinition
from .parameters import MultiValueParameter, Parameter, SingleValueParameter

__all__ = [
    "DimensionDefinition",
    "ParameterDefinition",
    "TermDefinition",
    "MultiValueParameter",
    "Parameter",
    "SingleValueParameter",
]
