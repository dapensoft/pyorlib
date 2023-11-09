from pyorlib.mp.engines.cplex import CplexEngine
from pyorlib.mp.engines.gurobi import GurobiEngine
from pyorlib.mp.engines.ortools import ORToolsEngine
from pyorlib.mp.engines.pulp import PuLPEngine


class EngineFixtures:
    @staticmethod
    def get_cplex_engine():
        return CplexEngine()

    @staticmethod
    def get_gurobi_engine():
        return GurobiEngine()

    @staticmethod
    def get_pulp_engine():
        return PuLPEngine()

    @staticmethod
    def get_or_tools_engine():
        return ORToolsEngine()
