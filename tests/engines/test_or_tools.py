import pytest

from pyorlib.enums import ValueType, SolutionStatus
from pyorlib.exceptions import TermException
from tests.engines.test_engine import TestEngine, TestEngineVariable
from tests.fixtures import EngineFixtures


class TestORToolsEngine:

    def test_variable_solver_assertions(self) -> None:
        variable_cls = EngineFixtures.get_or_tools_engine_cls()._Variable
        with pytest.raises(EngineFixtures.get_or_tools_exception_cls()):
            variable_cls(
                name="Test solver assertions",
                solver=None,
                solution_status=lambda *args, **kwargs: SolutionStatus.NOT_SOLVED,
                value_type=ValueType.CONTINUOUS,
            )

    def test_variable_value_type_assertions(self) -> None:
        variable_cls = EngineFixtures.get_or_tools_engine_cls()._Variable
        expected_exception = EngineFixtures.get_or_tools_exception_cls()
        solver = type("test", (object,), {})()
        solver.NumVar = lambda *args, **kwargs: None
        # Test variable value type not None assertion
        with pytest.raises(TermException):
            variable_cls(
                name="Test value type assertions",
                solver=solver,
                solution_status=lambda *args, **kwargs: SolutionStatus.NOT_SOLVED,
                value_type=None,
            )
        # Tests variable value type correctness assertion
        with pytest.raises(expected_exception):
            variable_cls(
                name="Test value type assertions",
                solver=solver,
                solution_status=lambda *args, **kwargs: SolutionStatus.NOT_SOLVED,
                value_type=11,
            )
        # Test variable creation
        with pytest.raises(expected_exception):
            variable_cls(
                name="Test value type assertions",
                solver=solver,
                solution_status=lambda *args, **kwargs: SolutionStatus.FEASIBLE,
                value_type=ValueType.CONTINUOUS,
            )
        # Test solution status assertion
        with pytest.raises(expected_exception):
            variable_cls(
                name="Test value type assertions",
                solver=solver,
                solution_status=None,
                value_type=ValueType.CONTINUOUS,
            )

    def test_variable_value_assertions(self):
        TestEngineVariable.variable_value_assertions(engine=EngineFixtures.get_or_tools_engine())

    def test_solver_assertions(self):
        TestEngine.solver_assertion_assertions(
            engine_cls=EngineFixtures.get_or_tools_engine_cls(),
            expected_exception=EngineFixtures.get_or_tools_exception_cls(),
        )
        EngineFixtures.get_or_tools_engine_cls()

    def test_objetive_function_assertions(self):
        TestEngine.objective_function_assertions(
            engine=EngineFixtures.get_or_tools_engine(), expected_exception=EngineFixtures.get_or_tools_exception_cls()
        )
