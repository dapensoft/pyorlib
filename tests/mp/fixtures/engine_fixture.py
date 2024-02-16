from pyorlib.mp.engines.cplex import CplexEngine
from pyorlib.mp.engines.gurobi import GurobiEngine
from pyorlib.mp.engines.ortools import ORToolsEngine
from pyorlib.mp.engines.pulp import PuLPEngine


class EngineFixtures:
    @staticmethod
    def get_cplex_engine() -> CplexEngine:
        """
        Returns an instance of the CplexEngine.
        :return: An instance of the CplexEngine.
        """
        return CplexEngine()

    @staticmethod
    def get_gurobi_engine() -> GurobiEngine:
        """
        Returns an instance of the GurobiEngine.
        :return: An instance of the GurobiEngine.
        """
        return GurobiEngine()

    @staticmethod
    def get_pulp_engine() -> PuLPEngine:
        """
        Returns an instance of the PuLPEngine.
        :return: An instance of the PuLPEngine.
        """
        return PuLPEngine()

    @staticmethod
    def get_or_tools_engine() -> ORToolsEngine:
        """
        Returns an instance of the ORToolsEngine.
        :return: An instance of the ORToolsEngine.
        """
        return ORToolsEngine()
