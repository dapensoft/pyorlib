"""
The Exceptions module in PyORlib provides a set of exception classes for handling specific errors and exceptions that
may occur during the usage of the library.
"""

from .cplex_exception import CplexException
from .gurobi_exception import GurobiException
from .model_exception import ModelException
from .ortools_exception import ORToolsException
from .pulp_exception import PuLPException
from .term_exception import TermException
