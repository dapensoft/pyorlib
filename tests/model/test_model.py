from math import inf
from typing import List

from pytest import raises

from pyorlib import Model, Engine
from pyorlib.algebra import Term, Element
from pyorlib.enums import ValueType, TermType, OptimizationType, SolutionStatus
from tests.fixtures import EngineFixtures


class TestModel:

    def test_model_creation(self):
        with raises(Exception):
            Model(engine=None)

    def test_float_precision_property(self):
        # Create Model
        model = Model(engine=EngineFixtures.get_cplex_engine(), float_precision=3)

        # Validate float precision getter
        assert model.float_precision == 3

        # Validate float precision setter
        model.float_precision = -5
        assert model.float_precision == 0

    @staticmethod
    def name_assertions(engine: Engine):
        model_name: str = "ModelName"
        model: Model = Model(engine=engine, name=model_name)
        assert model.name == model_name

    @staticmethod
    def dimension_assertions(engine: Engine):
        model: Model = Model(engine=engine)
        dimension_name: str = "r"

        # Validates negative values
        with raises(Exception):
            model.add_dimension(name=dimension_name, value=-1)

        # Validates zero values
        with raises(Exception):
            model.add_dimension(name=dimension_name, value=0)

        # Validate with empty name
        dimension_value: int = 2
        with raises(Exception):
            model.add_dimension(name="", value=dimension_value)

        # Validates creation and value
        model.add_dimension(name=dimension_name, value=dimension_value)
        assert model.get_dimension_by_name(name=dimension_name) == dimension_value

        # Verifies get method
        assert model.dimensions[dimension_name] == model.get_dimension_by_name(name=dimension_name)

        # Validates dimension overriding
        dimension_value = 5
        model.add_dimension(name=dimension_name, value=dimension_value)
        assert model.get_dimension_by_name(name=dimension_name) == dimension_value
        assert len(model.dimensions.items()) == 1

        # Multi dimension validation
        model.add_dimension(name="s", value=1)
        model.add_dimension(name="t", value=6)
        model.add_dimension(name="d", value=8)
        assert len(model.dimensions.items()) == 4
        assert model.get_dimension_by_name(name=dimension_name) == dimension_value
        assert model.get_dimension_by_name(name="s") == 1
        assert model.get_dimension_by_name(name="t") == 6
        assert model.get_dimension_by_name(name="d") == 8

        # Validates dimension dictionary overriding
        with raises(Exception):
            model.dimensions = {}

    @staticmethod
    def constant_terms_assertions(engine: Engine):
        model: Model = Model(engine=engine)
        constant_name: str = "c_1"

        # Validates constant creation
        const1 = model.add_constant(name=constant_name, value_type=ValueType.INTEGER, value=8)
        assert id(model.get_term_by_name(name=constant_name)) == id(model.terms[constant_name]) == id(const1)
        constant: Term = model.get_term_by_name(name=constant_name)

        # Validate constant values
        assert constant.value == constant.lower_bound == constant.upper_bound == 8
        assert constant.value_type == ValueType.INTEGER
        assert constant.term_type == TermType.CONSTANT

        # Validates duplicate constants
        with raises(Exception):
            model.add_constant(name=constant_name, value_type=ValueType.INTEGER, value=0)

        # Validates terms length
        assert len(model.terms.items()) == 1

    @staticmethod
    def variable_terms_assertions(engine: Engine):
        model: Model = Model(engine=engine)
        variable_name: str = "x_1"

        # Validates variables creation
        var1 = model.add_variable(name=variable_name, value_type=ValueType.BINARY)
        assert id(model.get_term_by_name(name=variable_name)) == id(model.terms[variable_name]) == id(var1)
        assert model.get_term_by_name(name=variable_name).lower_bound == 0
        assert model.get_term_by_name(name=variable_name).upper_bound == 1
        assert model.get_term_by_name(name=variable_name).value == -0.0
        assert model.get_term_by_name(name=variable_name).value_type == ValueType.BINARY
        assert model.get_term_by_name(name=variable_name).term_type == TermType.VARIABLE

        # Validates duplicate variables
        with raises(Exception):
            model.add_variable(name=variable_name, value_type=ValueType.BINARY)

        # Validates terms length
        assert len(model.terms.items()) == 1

        # Validates terms dictionary overriding
        with raises(Exception):
            model.terms = {}

    @staticmethod
    def constant_term_sets_assertions(engine: Engine):
        model: Model = Model(engine=engine)
        constants_set_name: str = "c_i_j"
        i_max: int = 4
        j_max: int = 2

        for i in range(i_max):
            for j in range(j_max):
                const1 = model.add_constant_to_set(
                    set_name=constants_set_name,
                    set_index=(i, j),
                    const_name=f"c_{i}_{j}",
                    value_type=ValueType.INTEGER,
                    value=i * j,
                )

                constant: Term = model.get_term_set_by_name(name=constants_set_name)[i, j]

                # Validates constant creation
                assert constant.value == constant.lower_bound == constant.upper_bound == i * j
                assert id(constant) == id(model.term_sets[constants_set_name][i, j]) == id(const1)
                assert id(constant) == id(model.terms[f"c_{i}_{j}"]) == id(const1)
                assert constant.value_type == ValueType.INTEGER
                assert constant.term_type == TermType.CONSTANT

        # Validates empty set name
        with raises(Exception):
            model.add_constant_to_set(
                set_name="", set_index=(5, 1), const_name="c_5_1", value_type=ValueType.BINARY, value=1
            )

        # Validates duplicate name
        with raises(Exception):
            model.add_constant_to_set(
                set_name=constants_set_name, set_index=(5, 1), const_name="c_1_1", value_type=ValueType.BINARY, value=1
            )

        # Validates duplicate index
        with raises(Exception):
            model.add_constant_to_set(
                set_name=constants_set_name, set_index=(1, 1), const_name="c_5_1", value_type=ValueType.BINARY, value=1
            )

        assert len(model.terms.items()) == len(model.get_term_set_by_name(name=constants_set_name)) == i_max * j_max
        assert model.term_sets[constants_set_name] == model.get_term_set_by_name(name=constants_set_name)
        assert len(model.term_sets) == 1

    @staticmethod
    def variable_term_sets_assertions(engine: Engine):
        model: Model = Model(engine=engine)
        variables_set_name: str = "x_i_j"
        i_max: int = 3
        j_max: int = 2

        for i in range(i_max):
            for j in range(j_max):
                var1 = model.add_variable_to_set(
                    set_name=variables_set_name,
                    set_index=(i, j),
                    var_name=f"x_{i}_{j}",
                    value_type=ValueType.BINARY,
                )
                variable: Term = model.get_term_set_by_name(name=variables_set_name)[i, j]

                # Validates variable creation
                assert id(variable) == id(model.term_sets[variables_set_name][i, j]) == id(var1)
                assert id(variable) == id(model.terms[f"x_{i}_{j}"]) == id(var1)
                assert variable.lower_bound == 0
                assert variable.upper_bound == 1
                assert variable.value == -0.0
                assert variable.value_type == ValueType.BINARY
                assert variable.term_type == TermType.VARIABLE

        # Validates empty names
        with raises(Exception):
            model.add_variable_to_set(
                set_name="",
                set_index=(4, 1),
                var_name="x_4_1",
                value_type=ValueType.BINARY,
            )

        # Validates duplicate name
        with raises(Exception):
            model.add_variable_to_set(
                set_name=variables_set_name,
                set_index=(4, 1),
                var_name="x_1_1",
                value_type=ValueType.BINARY,
            )

        # Validates duplicate index
        with raises(Exception):
            model.add_variable_to_set(
                set_name=variables_set_name,
                set_index=(1, 1),
                var_name="x_4_1",
                value_type=ValueType.BINARY,
            )

        assert len(model.terms.items()) == len(model.get_term_set_by_name(name=variables_set_name)) == i_max * j_max
        assert model.term_sets[variables_set_name] == model.get_term_set_by_name(name=variables_set_name)
        assert len(model.term_sets) == 1

    @staticmethod
    def constraint_assertions(engine: Engine):
        model: Model = Model(engine=engine)

        variable_name = "x"
        variable = model.add_variable(name=variable_name, value_type=ValueType.BINARY, lower_bound=0, upper_bound=1)

        model.add_constraint(expression=variable * 10 <= 800)
        model.add_constraint(expression=variable >= 5)
        assert len(model.constraints) == 2

        assert isinstance(model.constraints, List)
        assert len(model.constraints) == 2
        assert isinstance(model.constraints[0], Element)

    @staticmethod
    def objective_assertions(engine: Engine, opt_type: OptimizationType):
        model: Model = Model(engine=engine)

        variable_name_1 = "x_1"
        variable1 = model.add_variable(name=variable_name_1, value_type=ValueType.BINARY)

        with raises(Exception):
            none_variable = model.get_term_by_name(name="None")
            model.set_objective(opt_type=opt_type, expression=none_variable * 2 + 2)

        model.set_objective(opt_type=opt_type, expression=variable1 * 2 + 2)

        assert model.objective_value is None
        assert isinstance(model.objective_expr, Element)

    @staticmethod
    def optimal_resolution_assertions(engine: Engine):
        # Create a Model instance using the PuLP engine
        model: Model = Model(engine=engine)

        # Add two integer variables for coordinates x and y
        x = model.add_variable("x", ValueType.INTEGER, 0, inf)
        y = model.add_variable("y", ValueType.INTEGER, 0, inf)

        # Define problem constraints
        model.add_constraint(x + 7 * y <= 17.5)
        model.add_constraint(x <= 3.5)

        # Set objective to maximize x + 10y
        model.set_objective(OptimizationType.MAXIMIZE, x + 10 * y)

        # Checks empty objective value
        assert model.objective_value is None
        assert model.solution_status == SolutionStatus.NOT_SOLVED

        # Solve model
        model.solve()

        # Validate solution
        assert model.solution_status == SolutionStatus.OPTIMAL
        assert model.objective_value == 23
        assert x.value == 3
        assert y.value == 2

    @staticmethod
    def infeasible_resolution_assertions(engine: Engine):
        # Test infeasible model
        model: Model = Model(engine=engine)

        # Crates the variables
        variable_name_3 = "x_3"
        variable3 = model.add_variable(name=variable_name_3, value_type=ValueType.BINARY)

        variable_name_4 = "x_4"
        variable4 = model.add_variable(name=variable_name_4, value_type=ValueType.BINARY)

        # Sets the objective expression
        model.set_objective(opt_type=OptimizationType.MINIMIZE, expression=variable3 * 2 + variable4 * -1 + 2)

        # Infeasible constraint
        model.add_constraint(expression=variable3 * 2 >= 5)

        # Checks empty objective value
        assert model.objective_value is None
        assert model.solution_status == SolutionStatus.NOT_SOLVED

        # Solves the model
        model.solve()

        # Validate solution
        assert model.solution_status == SolutionStatus.INFEASIBLE

    class TestModelWithCplex:
        def test_model_name(self):
            TestModel.name_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_model_dimensions(self):
            TestModel.dimension_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_constant_terms(self):
            TestModel.constant_terms_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_variable_terms(self):
            TestModel.variable_terms_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_constant_term_sets(self):
            TestModel.constant_term_sets_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_variable_term_sets(self):
            TestModel.variable_term_sets_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_constraints(self):
            TestModel.constraint_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_set_objetive_minimize(self):
            TestModel.objective_assertions(engine=EngineFixtures.get_cplex_engine(), opt_type=OptimizationType.MINIMIZE)

        def test_set_objetive_maximize(self):
            TestModel.objective_assertions(engine=EngineFixtures.get_cplex_engine(), opt_type=OptimizationType.MAXIMIZE)

        def test_optimal_resolution(self):
            TestModel.optimal_resolution_assertions(engine=EngineFixtures.get_cplex_engine())

        def test_infeasible_resolution(self):
            TestModel.infeasible_resolution_assertions(engine=EngineFixtures.get_cplex_engine())

    class TestModelWithGurobi:
        def test_model_name(self):
            TestModel.name_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_model_dimensions(self):
            TestModel.dimension_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_constant_terms(self):
            TestModel.constant_terms_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_variable_terms(self):
            TestModel.variable_terms_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_constant_term_sets(self):
            TestModel.constant_term_sets_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_variable_term_sets(self):
            TestModel.variable_term_sets_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_constraints(self):
            TestModel.constraint_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_set_objetive_minimize(self):
            TestModel.objective_assertions(
                engine=EngineFixtures.get_gurobi_engine(), opt_type=OptimizationType.MINIMIZE
            )

        def test_set_objetive_maximize(self):
            TestModel.objective_assertions(
                engine=EngineFixtures.get_gurobi_engine(), opt_type=OptimizationType.MAXIMIZE
            )

        def test_optimal_resolution(self):
            TestModel.optimal_resolution_assertions(engine=EngineFixtures.get_gurobi_engine())

        def test_infeasible_resolution(self):
            TestModel.infeasible_resolution_assertions(engine=EngineFixtures.get_gurobi_engine())

    class TestModelWithORTools:
        def test_model_name(self):
            TestModel.name_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_model_dimensions(self):
            TestModel.dimension_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_constant_terms(self):
            TestModel.constant_terms_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_variable_terms(self):
            TestModel.variable_terms_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_constant_term_sets(self):
            TestModel.constant_term_sets_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_variable_term_sets(self):
            TestModel.variable_term_sets_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_constraints(self):
            TestModel.constraint_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_set_objetive_minimize(self):
            TestModel.objective_assertions(
                engine=EngineFixtures.get_or_tools_engine(), opt_type=OptimizationType.MINIMIZE
            )

        def test_set_objetive_maximize(self):
            TestModel.objective_assertions(
                engine=EngineFixtures.get_or_tools_engine(), opt_type=OptimizationType.MAXIMIZE
            )

        def test_optimal_resolution(self):
            TestModel.optimal_resolution_assertions(engine=EngineFixtures.get_or_tools_engine())

        def test_infeasible_resolution(self):
            TestModel.infeasible_resolution_assertions(engine=EngineFixtures.get_or_tools_engine())

    class TestModelWithPuLP:
        def test_model_name(self):
            TestModel.name_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_model_dimensions(self):
            TestModel.dimension_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_constant_terms(self):
            TestModel.constant_terms_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_variable_terms(self):
            TestModel.variable_terms_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_constant_term_sets(self):
            TestModel.constant_term_sets_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_variable_term_sets(self):
            TestModel.variable_term_sets_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_constraints(self):
            TestModel.constraint_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_set_objetive_minimize(self):
            TestModel.objective_assertions(engine=EngineFixtures.get_pulp_engine(), opt_type=OptimizationType.MINIMIZE)

        def test_set_objective_maximize(self):
            TestModel.objective_assertions(engine=EngineFixtures.get_pulp_engine(), opt_type=OptimizationType.MAXIMIZE)

        def test_optimal_resolution(self):
            TestModel.optimal_resolution_assertions(engine=EngineFixtures.get_pulp_engine())

        def test_infeasible_resolution(self):
            TestModel.infeasible_resolution_assertions(engine=EngineFixtures.get_pulp_engine())
