"""
A powerful Python library for operations research. Define, solve, and interact with
mathematical models in a standardized manner across different optimization packages.
"""

__version__ = "0.1.0"

from .mp.algebra import Element
from .mp.algebra.expressions import Expression
from .mp.algebra.terms import Term
from .mp.algebra.terms.constants import Constant
from .mp.algebra.terms.variables import Variable
from .mp.engines import Engine
from .mp.enums import OptimizationType, ParameterType, SolutionStatus, TermType, ValueType
from .mp.exceptions import CplexException, GurobiException, ModelException, ORToolsException, PuLPException, \
    TermException
from .mp.model import Model
from .mp.structures.definitions import DimensionDefinition, ParameterDefinition, TermDefinition
from .mp.structures.parameters import Parameter, MultiValueParameter, SingleValueParameter
from .mp.validators import ValueTypeValidator
from .mp.validators.fields import DimensionField, ParameterField

__all__ = [
    "Element",
    "Expression",
    "Term",
    "Constant",
    "Variable",
    "Engine",
    "OptimizationType",
    "ParameterType",
    "SolutionStatus",
    "TermType",
    "ValueType",
    "CplexException",
    "GurobiException",
    "ModelException",
    "ORToolsException",
    "PuLPException",
    "TermException",
    "Model",
    "DimensionDefinition",
    "ParameterDefinition",
    "TermDefinition",
    "Parameter",
    "MultiValueParameter",
    "SingleValueParameter",
    "ValueTypeValidator",
    "DimensionField",
    "ParameterField",
]
