from math import inf

from pytest import raises

from pyorlib.algebra import Term, Variable
from pyorlib.engines import Engine
from pyorlib.enums import ValueType, TermType
from tests.fixtures import EngineFixtures


class TestVariable:

    def test_inheritance(self):
        assert issubclass(Variable, Term)

    class TestBinaryVariables:
        def assertions(self, solver: Engine):
            var_name: str = "x_1"
            var1: Term = solver.add_variable(name=var_name, value_type=ValueType.BINARY)

            assert var1 is not None
            assert isinstance(var1, Variable)
            assert var1.raw is not None
            assert var1.name == var_name
            assert var1.value_type == ValueType.BINARY
            assert var1.term_type == TermType.VARIABLE and var1.is_variable and not var1.is_constant
            assert var1.lower_bound == 0 and var1.upper_bound == 1
            assert var1.value == -0.0

            # Validates empty name
            with raises(Exception):
                solver.add_variable(name="", value_type=ValueType.BINARY)

            # Validates when the lower bound is None
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=ValueType.BINARY, lower_bound=None)

            # Validates when the upper bound is None
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=ValueType.BINARY, upper_bound=None)

            # Validates invalid lower bound
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=ValueType.BINARY, lower_bound=-2)

            # Validates invalid upper bound
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=ValueType.BINARY, upper_bound=2)

            # Validates when the lower bound is greater than the upper bound
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=ValueType.BINARY, lower_bound=1, upper_bound=0)

            # Validates None at value type
            with raises(Exception):
                solver.add_variable(name=var_name, value_type=None)

        def test_creation_cplex(self):
            self.assertions(solver=EngineFixtures.get_cplex_engine())

        def test_creation_gurobi(self):
            self.assertions(solver=EngineFixtures.get_gurobi_engine())

        def test_creation_or_tools(self):
            self.assertions(solver=EngineFixtures.get_or_tools_engine())

        def test_creation_pulp(self):
            self.assertions(solver=EngineFixtures.get_pulp_engine())

    class TestIntegerVariables:
        def assertions(self, solver: Engine):
            # Validates default values
            var_name1: str = "x_1"
            var1: Term = solver.add_variable(name=var_name1, value_type=ValueType.INTEGER)

            assert var1 is not None
            assert isinstance(var1, Variable)
            assert var1.raw is not None
            assert var1.name == var_name1
            assert var1.value_type == ValueType.INTEGER
            assert var1.term_type == TermType.VARIABLE and var1.is_variable and not var1.is_constant
            assert var1.lower_bound == 0 and var1.upper_bound == inf
            assert var1.value == -0.0

            # Validates infinity values
            var_name2: str = "x_2"
            var2 = solver.add_variable(name=var_name2, value_type=ValueType.INTEGER, lower_bound=-inf, upper_bound=inf)
            assert var2.lower_bound == -inf and var2.upper_bound == inf
            assert var2.value == -0.0

            # Validates non default values
            var_name3: str = "x_3"
            var3 = solver.add_variable(name=var_name3, value_type=ValueType.INTEGER, lower_bound=4, upper_bound=5)
            assert var3.lower_bound == 4 and var3.upper_bound == 5
            assert var3.value == -0.0

            # Validates equal values
            var_name4: str = "x_4"
            var4 = solver.add_variable(name=var_name4, value_type=ValueType.INTEGER, lower_bound=4, upper_bound=4)
            assert var4.lower_bound == 4 and var4.upper_bound == 4
            assert var4.value == -0.0

            # Validates empty name
            with raises(Exception):
                solver.add_variable(name="", value_type=ValueType.INTEGER)

            # Validates when the lower bound is None
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, lower_bound=None)

            # Validates when the upper bound is None
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, upper_bound=None)

            # Validates infinity
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, lower_bound=inf)

            # Validates -infinity
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, upper_bound=-inf)

            # Validates lower and upper bounds
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, lower_bound=5, upper_bound=4)

            # Validates non integer lower bound
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, lower_bound=1.1)

            # Validates non integer upper bound
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.INTEGER, upper_bound=4.5)

            # Validates None at value type
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=None)

        def test_creation_cplex(self):
            self.assertions(solver=EngineFixtures.get_cplex_engine())

        def test_creation_gurobi(self):
            self.assertions(solver=EngineFixtures.get_gurobi_engine())

        def test_creation_or_tools(self):
            self.assertions(solver=EngineFixtures.get_or_tools_engine())

        def test_creation_pulp(self):
            self.assertions(solver=EngineFixtures.get_pulp_engine())

    class TestContinuousVariables:
        def assertions(self, solver: Engine):
            # Validate default values
            var_name1: str = "x_1"
            var1: Term = solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS)

            assert var1 is not None
            assert isinstance(var1, Variable)
            assert var1.raw is not None
            assert var1.name == var_name1
            assert var1.value_type == ValueType.CONTINUOUS
            assert var1.term_type == TermType.VARIABLE and var1.is_variable and not var1.is_constant
            assert var1.lower_bound == 0.0 and var1.upper_bound == inf
            assert var1.value == -0.0

            # Validates infinity values
            var_name2: str = "x_2"
            var2 = solver.add_variable(
                name=var_name2, value_type=ValueType.CONTINUOUS, lower_bound=-inf, upper_bound=inf
            )
            assert var2.lower_bound == -inf and var2.upper_bound == inf
            assert var2.value == -0.0

            # Validates non default values
            var_name3: str = "x_3"
            var3 = solver.add_variable(name=var_name3, value_type=ValueType.CONTINUOUS, lower_bound=4, upper_bound=4.1)
            assert var3.lower_bound == 4 and var3.upper_bound == 4.1
            assert var3.value == -0.0

            # Validates equal values
            var_name4: str = "x_4"
            var4 = solver.add_variable(
                name=var_name4, value_type=ValueType.CONTINUOUS, lower_bound=4.5, upper_bound=4.5
            )
            assert var4.lower_bound == 4.5 and var4.upper_bound == 4.5
            assert var4.value == -0.0

            # Validates empty name
            with raises(Exception):
                solver.add_variable(name="", value_type=ValueType.CONTINUOUS)

            # Validates when the lower bound is None
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS, lower_bound=None)

            # Validates when the upper bound is None
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS, upper_bound=None)

            # Validates infinity
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS, lower_bound=inf)

            # Validates -infinity
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS, upper_bound=-inf)

            # Validates lower and upper bounds
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=ValueType.CONTINUOUS, lower_bound=4.2, upper_bound=4.1)

            # Validates None at value type
            with raises(Exception):
                solver.add_variable(name=var_name1, value_type=None)

        def test_creation_cplex(self):
            self.assertions(solver=EngineFixtures.get_cplex_engine())

        def test_creation_gurobi(self):
            self.assertions(solver=EngineFixtures.get_gurobi_engine())

        def test_creation_or_tools(self):
            self.assertions(solver=EngineFixtures.get_or_tools_engine())

        def test_creation_pulp(self):
            self.assertions(solver=EngineFixtures.get_pulp_engine())
