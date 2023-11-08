from typing import Dict, Tuple, List, Mapping
from uuid import uuid4

from pyorlib.core.loggers import Logger
from pyorlib.core.utils import StdOutColors
from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.common.exceptions import ModelException
from pyorlib.mp.engines import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.terms import Term
from pyorlib.mp.math.terms.constants import Constant
from pyorlib.mp.math.terms.variables import Variable


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

    def get_dimension_by_name(self, name: str) -> int:
        """
        Returns the size of a dimension in the model by name.
        :param name: The name of the dimension.
        :return: The size of the dimension, or 0 if the dimension does not exist.
        """
        return self._dimensions.get(name, 0)

    def get_term_by_name(self, name: str) -> Term | None:
        """
        Returns a term in the model by name.
        :param name: The name of the term.
        :return: The term, or `None` if the term does not exist.
        """
        return self._terms.get(name, None)

    def get_term_set_by_name(self, name: str) -> Mapping[Tuple[int, ...], Term] | None:
        """
        Returns a set of terms in the model by name.
        :param name: The name of the set.
        :return: The set of terms, or `None` if the set does not exist.
        """
        return self._term_sets.get(name, None)

    def add_dimension(self, name: str, value: int) -> int:
        """
        Adds a new dimension to the model.
        :param name: The name of the dimension to be added.
        :param value: The size of the new dimension.
        :return: The dimension added to the model.
        """
        if not name or value is None or not isinstance(value, int) or value < 1:
            raise ModelException("Invalid dimension values.")
        self._dimensions[name] = value

        if self._logger.debug_enabled:
            self._logger.debug(
                action="Dimension added: ",
                msg="".join([
                    f"Name: {StdOutColors.PURPLE}{name}{StdOutColors.DEFAULT} | ",
                    f"val: {StdOutColors.PURPLE}{value}{StdOutColors.DEFAULT}",
                ]),
            )

        return value

    def add_constant(self, name: str, value_type: ValueType, value: float) -> Constant:
        """
        Adds a new constant to the model.
        :param name: The name of the constant to be added.
        :param value_type: The type of the constant value.
        :param value: The constant value.
        :return: The constant added to the model.
        """
        if name in self.terms:
            raise ModelException(f"Duplicate term with name: {name}")

        constant: Constant = Constant(name=name, value_type=value_type, value=value)

        self.__save_term(term=constant)

        if self._logger.debug_enabled:
            self._logger.debug(
                action="Constant added: ",
                msg=constant.get_pretty_string(float_precision=self.float_precision),
            )

        return constant

    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None,
    ) -> Variable:
        """
        Adds a new variable to the model.
        :param name: The name of the variable to be added.
        :param value_type: The type of the variable values.
        :param lower_bound: The lower bound of the variable. If not specified, the default value is 0.
        :param upper_bound: The upper bound of the variable. If not specified, the default value is infinity.
        :return: The variable added to the model.
        """
        if name in self.terms:
            raise ModelException(f"Duplicate term with name: {name}")

        variable: Variable = self._engine.add_variable(
            name=name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound
        )

        self.__save_term(term=variable)

        if self._logger.debug_enabled:
            self._logger.debug(
                action="Variable added: ",
                msg=variable.get_pretty_string(float_precision=self.float_precision),
            )

        return variable

    def add_constant_to_set(
            self,
            set_name: str,
            set_index: Tuple[int, ...],
            const_name: str,
            value_type:
            ValueType,
            value: float,
    ) -> Constant:
        """
        Adds a new constant to the model within a set.
        :param set_name: The name of the set where the constant will be added.
        :param set_index: The position of a term within a set representing its indices.
        :param const_name: The name of the constant to be saved.
        :param value_type: The type of the constant value.
        :param value: The constant value.
        :return: The constant added to the model.
        """
        if const_name in self.terms:
            raise ModelException(f"Duplicate term with name: {const_name}")

        if set_name in self.term_sets and set_index in self.term_sets[set_name]:
            raise ModelException(f"Duplicate set name and index: {set_name} | {set_index}")

        constant: Constant = Constant(name=const_name, value_type=value_type, value=value)

        self.__save_term_to_set(set_name=set_name, set_index=set_index, term=constant)

        if self._logger.debug_enabled:
            self._logger.debug(
                action="Constant added to set: ",
                msg="".join([
                    f"Set name: {StdOutColors.PURPLE}{set_name}{StdOutColors.DEFAULT} | ",
                    f"Set index: {StdOutColors.PURPLE}{set_index}{StdOutColors.DEFAULT} | ",
                    constant.get_pretty_string(float_precision=self.float_precision)
                ]),
            )

        return constant

    def add_variable_to_set(
            self,
            set_name: str,
            set_index: Tuple[int, ...],
            var_name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None,
    ) -> Variable:
        """
        Adds a new variable to the model within a set.
        :param set_name: The name of the set where the variable will be added.
        :param set_index: The position of a term within a set that represents its indices.
        :param var_name: The name of the variable to be added.
        :param value_type: The type of the variable values.
        :param lower_bound: The lower bound of the variable. If not specified, the default value is 0.
        :param upper_bound: The upper bound of the variable. If not specified, the default value is infinity.
        :return: The variable added to the model.
        """
        if var_name in self.terms:
            raise ModelException(f"Duplicate term with name: {var_name}")

        if set_name in self.term_sets and set_index in self.term_sets[set_name]:
            raise ModelException(f"Duplicate set name and index: {set_name} | {set_index}")

        variable: Variable = self._engine.add_variable(
            name=var_name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound
        )

        self.__save_term_to_set(set_name=set_name, set_index=set_index, term=variable)

        if self._logger.debug_enabled:
            self._logger.debug(
                action="Variable added to set: ",
                msg="".join([
                    f"Set name: {StdOutColors.PURPLE}{set_name}{StdOutColors.DEFAULT} | ",
                    f"Set index: {StdOutColors.PURPLE}{set_index}{StdOutColors.DEFAULT} | ",
                    variable.get_pretty_string(float_precision=self.float_precision)
                ]),
            )

        return variable

    def add_constraint(self, expression: Element) -> Element:
        """
        Adds a new constraint to the model. When working with model's terms in symbolic algebra systems,
        it is necessary to use the `Term.expr` method to perform mathematical operations with them.
        :param expression: The expression that the constraint must satisfy.
        :return: An object representing the constraint.
        """
        constraint: Element = self._engine.add_constraint(expression=expression)

        if self._logger.debug_enabled:
            try:
                self._logger.debug(action="Constraint added: ", msg=f"Expr: {expression}")
            except RecursionError:
                self._logger.debug(action="Constraint added: ", msg="Expr: Unprintable expression")

        return constraint

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        """
        Sets the optimization objective for the model. When working with model's terms in symbolic algebra systems,
        it is necessary to use the `Term.expr` method to perform mathematical operations with them.
        :param opt_type: The type of optimization to be performed, such as 'maximize' or 'minimize'.
        :param expression: The expression to be optimized.
        :return: The objective function.
        """
        objective: Element = self._engine.set_objective(opt_type=opt_type, expression=expression)

        if self._logger.debug_enabled:
            try:
                self._logger.debug(
                    action="Objective function added: ",
                    msg="".join([
                        f"Opt Type: {StdOutColors.PURPLE}{opt_type.name.capitalize()}{StdOutColors.DEFAULT} | ",
                        f"Expr: {objective}"
                    ])
                )
            except RecursionError:
                self._logger.debug(action="Objective function added: ", msg="Expr: Unprintable expression")

        return objective

    def clear(self) -> None:
        """
        Clears the contents of the model.
        :return: None.
        """
        self._engine.clear()
        self._dimensions = {}
        self._terms = {}
        self._term_sets = {}

        if self._logger.debug_enabled:
            self._logger.debug(f"The model data has been cleared.")

    def solve(self) -> None:
        """
        Solves the optimization problem represented by the model.
        :return: None.
        """
        if self._logger.debug_enabled:
            self._logger.debug(f"Solving the model...")

        self._engine.solve()

        if self._logger.debug_enabled:
            self._logger.debug(f"The model has been solved.")

    def print_info(self, display_term_sets: bool = False) -> None:
        print(f"\n------ MODEL INFORMATION ------\n")
        print("Model properties:")
        print(f"\tName: {StdOutColors.PURPLE}{self.name}{StdOutColors.DEFAULT}")
        print("Objective function:")
        print(f"\tExpression: {self.objective_expr}")
        print(f"\tStatus: {StdOutColors.PURPLE}{self.solution_status.name}{StdOutColors.DEFAULT}")
        print(
            f"\tValue: {StdOutColors.PURPLE}",
            '{0:.{prec}g}'.format(self.objective_value,
                                  prec=self.float_precision) if self.objective_value is not None else "--",
            f"{StdOutColors.DEFAULT}"
        )

        print("Dimensions:")
        for name, size in self.dimensions.items():
            print(
                f"\tName: {StdOutColors.PURPLE}{name}{StdOutColors.DEFAULT} | ",
                f"Val: {StdOutColors.PURPLE}{size}{StdOutColors.DEFAULT}"
            )

        print("Terms:")
        for name, term in self.terms.items():
            print(f"\t{term.get_pretty_string(float_precision=self.float_precision)}")
        if display_term_sets:
            print("Terms Sets:")
            for name, terms in self.term_sets.items():
                print(f"\tTerm: {StdOutColors.PURPLE}{name}{StdOutColors.DEFAULT}")
                for index, term in terms.items():
                    print(
                        f"\t\tIndex: {StdOutColors.PURPLE}{index}{StdOutColors.DEFAULT} | ",
                        f"{term.get_pretty_string(float_precision=self.float_precision)}"
                    )

        print("Constraints:")
        constraints = self.constraints
        for exp in constraints:
            try:
                print(f"\tExpression: {exp}")
            except RecursionError:
                print("\tExpression: Unprintable expression")
        print()

    def print_solution(self) -> None:
        print(f"\n------ MODEL SOLUTION ------\n")
        print("Objective function:")
        print(f"\tStatus: {StdOutColors.PURPLE}{self.solution_status.name}{StdOutColors.DEFAULT}")
        print(
            f"\tValue: {StdOutColors.PURPLE}",
            '{0:.{prec}g}'.format(self.objective_value,
                                  prec=self.float_precision) if self.objective_value is not None else "--",
            f"{StdOutColors.DEFAULT}"
        )

        solution_variables: Dict[str, Term] = {
            name: term for name, term in self.terms.items() if (term.is_variable and term.value != 0)
        }

        if solution_variables:
            print("Terms:")
            for name, term in solution_variables.items():
                print(f"\t{term.get_pretty_string(float_precision=self.float_precision)}")

        print()
