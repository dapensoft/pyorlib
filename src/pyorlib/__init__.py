"""
A powerful Python library for operations research. Define, solve, and interact with
mathematical models in a standardized manner across different optimization packages.
"""

__version__ = "0.1.3"

from .engines import Engine
from .model import Model

__all__ = [
    "Engine",
    "Model",
]
