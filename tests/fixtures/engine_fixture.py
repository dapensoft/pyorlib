from typing import Type

from pyorlib.engines.cplex import CplexEngine
from pyorlib.engines.gurobi import GurobiEngine
from pyorlib.engines.ortools import ORToolsEngine
from pyorlib.engines.pulp import PuLPEngine
from pyorlib.exceptions import CplexException, GurobiException, PuLPException, ORToolsException


class EngineFixtures:
    @staticmethod
    def get_cplex_engine() -> CplexEngine:
        """
        Returns an instance of the CplexEngine.
        :return: An instance of the CplexEngine.
        """
        return CplexEngine()

    @staticmethod
    def get_cplex_engine_cls() -> Type[CplexEngine]:
        """
        Returns a class reference to CplexEngine.
        :return: A class reference to CplexEngine.
        """
        return CplexEngine

    @staticmethod
    def get_cplex_exception_cls() -> Type[CplexException]:
        """
        Returns a class reference to CplexException.
        :return: A class reference to CplexException.
        """
        return CplexException

    @staticmethod
    def get_gurobi_engine() -> GurobiEngine:
        """
        Returns an instance of the GurobiEngine.
        :return: An instance of the GurobiEngine.
        """
        return GurobiEngine()

    @staticmethod
    def get_gurobi_engine_cls() -> Type[GurobiEngine]:
        """
        Returns a class reference to GurobiEngine.
        :return: A class reference to GurobiEngine.
        """
        return GurobiEngine

    @staticmethod
    def get_gurobi_exception_cls() -> Type[GurobiException]:
        """
        Returns a class reference to GurobiException.
        :return: A class reference to GurobiException.
        """
        return GurobiException

    @staticmethod
    def get_pulp_engine() -> PuLPEngine:
        """
        Returns an instance of the PuLPEngine.
        :return: An instance of the PuLPEngine.
        """
        return PuLPEngine()

    @staticmethod
    def get_pulp_engine_cls() -> Type[PuLPEngine]:
        """
        Returns a class reference to PuLPEngine.
        :return: A class reference to PuLPEngine.
        """
        return PuLPEngine

    @staticmethod
    def get_pulp_exception_cls() -> Type[PuLPException]:
        """
        Returns a class reference to PuLPException.
        :return: A class reference to PuLPException.
        """
        return PuLPException

    @staticmethod
    def get_or_tools_engine() -> ORToolsEngine:
        """
        Returns an instance of the ORToolsEngine.
        :return: An instance of the ORToolsEngine.
        """
        return ORToolsEngine()

    @staticmethod
    def get_or_tools_engine_cls() -> Type[ORToolsEngine]:
        """
        Returns a class reference to PuLPEngine.
        :return: A class reference to PuLPEngine.
        """
        return ORToolsEngine

    @staticmethod
    def get_or_tools_exception_cls() -> Type[ORToolsException]:
        """
        Returns a class reference to PuLPException.
        :return: A class reference to PuLPException.
        """
        return ORToolsException
