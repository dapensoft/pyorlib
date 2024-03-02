from tests.engines.test_engine import TestEngineVariable, TestEngine
from tests.fixtures import EngineFixtures


class TestCplexEngine:

    def test_variable_solver_assertions(self):
        TestEngineVariable.variable_solver_assertions(
            variable_cls=EngineFixtures.get_cplex_engine_cls()._Variable,
            expected_exception=EngineFixtures.get_cplex_exception_cls(),
        )

    def test_variable_value_type_assertions(self):
        solver = type("test", (object,), {})()
        solver.continuous_var = lambda *args, **kwargs: None
        TestEngineVariable.variable_value_type_assertions(
            variable_cls=EngineFixtures.get_cplex_engine_cls()._Variable,
            solver=solver,
            expected_exception=EngineFixtures.get_cplex_exception_cls(),
        )

    def test_variable_value_assertions(self):
        TestEngineVariable.variable_value_assertions(engine=EngineFixtures.get_cplex_engine())

    def test_solver_assertions(self):
        TestEngine.solver_assertion_assertions(
            engine_cls=EngineFixtures.get_cplex_engine_cls(),
            expected_exception=EngineFixtures.get_cplex_exception_cls(),
        )

    def test_objective_function_assertions(self):
        TestEngine.objective_function_assertions(
            engine=EngineFixtures.get_cplex_engine(), expected_exception=EngineFixtures.get_cplex_exception_cls()
        )
