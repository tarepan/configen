"""Utilities."""

from typing import TypeVar
from copy import deepcopy
from dataclasses import field


# [Design Notes]
# Sugar syntax for mutable default argument.
# This function takes an instance (not a class) as the argument template, so needs deepcopy for immutability.

T = TypeVar("T")
def default(instance: T):
    """Dataclass field with template instance.
    
    Args:
        instance - Default argument template
    Returns:
                 - Class field with default_factory
    """
    return field(default_factory = lambda: deepcopy(instance))
