from typing import Type, Any

import pytest

from pyorlib.algebra import Variable
from pyorlib.core.exceptions import PyORlibException
from pyorlib.engines import Engine
from pyorlib.enums import ValueType
from pyorlib.exceptions import TermException


class TestEngine:

    @staticmethod
    def solver_assertion_assertions(engine_cls: Type[Engine], expected_exception: Type[PyORlibException]) -> None:
        with pytest.raises(expected_exception):
            engine_cls(solver=11)

    @staticmethod
    def objective_function_assertions(engine: Engine, expected_exception: Type[PyORlibException]):
        var1: Variable = engine.add_variable(name="Test variable", value_type=ValueType.CONTINUOUS)
        with pytest.raises(expected_exception):
            engine.set_objective(opt_type=None, expression=var1 <= 3)


class TestEngineVariable:

    @staticmethod
    def variable_solver_assertions(variable_cls: Type[Variable], expected_exception: Type[PyORlibException]) -> None:
        with pytest.raises(expected_exception):
            variable_cls(name="Test solver assertions", solver=None, value_type=ValueType.CONTINUOUS)

    @staticmethod
    def variable_value_type_assertions(
        variable_cls: Type[Variable], solver: Any, expected_exception: Type[PyORlibException]
    ) -> None:
        # Test variable value type not None assertion
        with pytest.raises(TermException):
            variable_cls(name="Test value type assertions", solver=solver, value_type=None)
        # Tests variable value type correctness assertion
        with pytest.raises(expected_exception):
            variable_cls(name="Test value type assertions", solver=solver, value_type=11)
        # Test variable creation
        with pytest.raises(expected_exception):
            variable_cls(name="Test value type assertions", solver=solver, value_type=ValueType.CONTINUOUS)

    @staticmethod
    def variable_value_assertions(engine: Engine) -> None:
        var = engine.add_variable(name="Test variable", value_type=ValueType.CONTINUOUS)
        assert var.value == -0.0
