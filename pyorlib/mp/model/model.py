from typing import Dict, Tuple, List, Mapping
from uuid import uuid4

from pyorlib.core.logger import Logger
from pyorlib.core.utils import StdOutColors
from pyorlib.mp.common.enums import SolutionStatus
from pyorlib.mp.common.exceptions import ModelException
from pyorlib.mp.engines import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.terms import Term


class Model:
    """ A base class to represent a mathematical programming model. """

    @property
    def name(self) -> str:
        """
        Returns the name of the model.
        :return: A string with the name of the model.
        """
        return self._name

    @property
    def dimensions(self) -> Mapping[str, int]:
        """
        Returns a dictionary with the dimensions and their sizes of the model.
        :return: A dictionary where the keys are dimension names and the values are their sizes.
        """
        return self._dimensions

    @property
    def constraints(self) -> List[Element]:
        """
        Returns a list with the constraints of the model.
        :return: A list of constraints.
        """
        return self._engine.constraints

    @property
    def terms(self) -> Mapping[str, Term]:
        """
        Returns a dictionary that contains the individual terms used in the model.
        :return: A dictionary where the keys represent the names of the terms and the values represent the
        terms themselves. A term may be a constant value or a variable.
        """
        return self._terms

    @property
    def term_sets(self) -> Mapping[str, Mapping[Tuple[int, ...], Term]]:
        """
        Returns a dictionary that contains the set of terms used in the model.
        :return: A dictionary where the keys represent the names of the sets and
        the values represent the sets themselves. Each set of terms is a dictionary
        with the indices of the terms as keys and the terms themselves as values.
        A term may be a constant value or a variable.
        """
        return self._term_sets

    @property
    def objective_value(self) -> float | None:
        """
        Returns the value of the objective function in the model.
        :return: The value of the objective function, or `None` if the model has not
        been solved or an objective function is not defined.
        """
        return self._engine.objective_value

    @property
    def objective_expr(self) -> Element | None:
        """
        Returns the expression of the objective function, if available.
        :return: The objective function, or None if not available.
        """
        return self._engine.objective_expr

    @property
    def solution_status(self) -> SolutionStatus:
        """
        Returns an enumeration that represents the state of the solution.
        :return: A SolutionStatus enumeration.
        """
        return self._engine.solution_status

    @property
    def float_precision(self) -> int:
        """
        This property is used to get or set the float precision of the model.
        The float precision is an integer number of digits, used in printing the solution and objective.
        :return: The current float precision of the solver.
        """
        return self._float_precision

    @float_precision.setter
    def float_precision(self, float_precision: int):
        num_digits: int = float_precision

        if float_precision < 0:
            self._logger.warning(f"Negative float precision given: {num_digits}, using 0 instead.")
            num_digits = 0

        self._float_precision: int = num_digits
        """ The float precision is an integer number of digits, used in printing the solution and objective. """

    def __init__(self, engine: Engine, name: str | None = None, debug: bool = False, float_precision: int = 6):
        """
        Initializes a new instance of the `Model` class.
        :param engine: The engine interface to be used for solving the model.
        :param name: An optional name for the model.
        :param debug: A flag indicating whether debug mode is enabled.
        :param float_precision: It represents the number of digits used in printing the solution and objective.
        """
        # Instance attributes
        self._name: str = name if name else f"model_{str(uuid4())}"
        """ A name for the model. """

        self._logger: Logger = Logger(self._name, debug)
        """ An object used for logging messages from the model. """

        self._engine: Engine = engine
        """ The engine interface used to solve the model. """

        self._dimensions: Dict[str, int] = {}
        """  
        A dictionary of the model's dimensions, where the keys are the 
        names of the dimensions and the values are their sizes.
        """

        self._terms: Dict[str, Term] = {}
        """ 
        A dictionary of individual terms used in the model, where the keys represent the names 
        of the terms and the values represent the terms themselves. A term may be a constant value 
        or a variable.
        """

        self._term_sets: Dict[
            str,
            Dict[
                Tuple[int, ...],
                Term
            ]
        ] = {}
        """
        A dictionary of term sets used in the model, where the keys represent the names 
        of the sets and the values represent the sets themselves. Each set of terms is a 
        dictionary with the indices of the terms as keys and the terms themselves as 
        values. A term may be a constant value or a variable.

        |

        Example:
        Z_r_s_t: {
            | (1, 1, 1): Variable,
            | (1, 1, 2): Constant,
            | (2, 1, 1): Variable,
        }
        """

        if self._engine is None:
            raise ModelException("Engine interface cannot be None.")

        if self._logger.debug_enabled:
            self._logger.debug(
                f"The '{StdOutColors.PURPLE}{self.name.capitalize()}{StdOutColors.DEFAULT}' has been created."
            )

        self.float_precision = float_precision

    def __save_term(self, term: Term) -> None:
        """
        Saves a single term in the model.
        :param term: The term to be saved.
        :return: None
        """
        self._terms[term.name] = term

    def __save_term_to_set(self, set_name: str, set_index: Tuple[int, ...], term: Term) -> None:
        """
        Saves a term into a set.
        :param set_name: The name of the set where the term will be saved.
        :param set_index: The index position of the term within a set in the model.
        :param term: The term to be saved.
        :return: None
        """
        if not set_name:
            raise ModelException("Set name cannot be empty.")

        self.__save_term(term)

        if set_name not in self._term_sets:
            self._term_sets[set_name] = {}

        self._term_sets[set_name][set_index] = term
