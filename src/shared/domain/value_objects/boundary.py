"""
Boundary abstraction for geographic boundaries.

This interface keeps domain objects free from concrete GIS libraries.
"""

from abc import ABC, abstractmethod


class Boundary(ABC):
    """Abstract representation of a geographic boundary."""

    @abstractmethod
    def is_empty(self) -> bool:
        """Return True when the boundary has no geometry/data."""
        raise NotImplementedError
