import pytest

from pyorlib.exceptions import TermException
from tests.engines.test_engine import TestEngineVariable, TestEngine
from tests.fixtures import EngineFixtures


class TestPuLPEngine:

    def test_variable_solver_assertions(self):
        TestEngineVariable.variable_solver_assertions(
            variable_cls=EngineFixtures.get_pulp_engine_cls()._Variable,
            expected_exception=EngineFixtures.get_pulp_exception_cls(),
        )

    def test_variable_value_type_assertions(self):
        solver = type("test", (object,), {})()
        solver.addVar = lambda *args, **kwargs: None
        variable_cls = EngineFixtures.get_pulp_engine_cls()._Variable
        expected_exception = EngineFixtures.get_pulp_exception_cls()
        # Test variable value type not None assertion
        with pytest.raises(TermException):
            variable_cls(name="Test value type assertions", solver=solver, value_type=None)
        # Tests variable value type correctness assertion
        with pytest.raises(expected_exception):
            variable_cls(name="Test value type assertions", solver=solver, value_type=11)

    def test_variable_value_assertions(self):
        TestEngineVariable.variable_value_assertions(engine=EngineFixtures.get_pulp_engine())

    def test_solver_assertions(self):
        TestEngine.solver_assertion_assertions(
            engine_cls=EngineFixtures.get_pulp_engine_cls(),
            expected_exception=EngineFixtures.get_pulp_exception_cls(),
        )

    def test_objetive_function_assertions(self):
        TestEngine.objective_function_assertions(
            engine=EngineFixtures.get_pulp_engine(), expected_exception=EngineFixtures.get_pulp_exception_cls()
        )
