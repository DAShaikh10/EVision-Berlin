"""
Demand Analysis Infrastructure Repositories module.
"""

from abc import ABC, abstractmethod

from src.shared.domain.value_objects import PostalCode
from src.demand.domain.aggregates import DemandAnalysisAggregate


class DemandAnalysisRepository(ABC):
    """
    Abstract base class for DemandAnalysisRepository.
    Defines the interface for accessing demand analysis data.

    Repository Pattern: Provides collection-like interface for aggregates.
    Encapsulates data access logic and persistence details.
    """

    @abstractmethod
    def save(self, aggregate: DemandAnalysisAggregate) -> None:
        """
        Save or update a demand analysis aggregate.

        Args:
            aggregate: DemandAnalysisAggregate to save
        """

    @abstractmethod
    def find_by_postal_code(self, postal_code: PostalCode) -> DemandAnalysisAggregate | None:
        """
        Find demand analysis by postal code.

        Args:
            postal_code: PostalCode to search for

        Returns:
            Optional[DemandAnalysisAggregate]: Found aggregate or None
        """

    @abstractmethod
    def find_all(self) -> list[DemandAnalysisAggregate]:
        """
        Find all demand analyses.

        Returns:
            List[DemandAnalysisAggregate]: All saved aggregates
        """

    @abstractmethod
    def delete(self, postal_code: PostalCode) -> bool:
        """
        Delete demand analysis by postal code.

        Args:
            postal_code: PostalCode to delete

        Returns:
            bool: True if deleted, False if not found
        """

    @abstractmethod
    def exists(self, postal_code: PostalCode) -> bool:
        """
        Check if demand analysis exists for postal code.

        Args:
            postal_code: PostalCode to check

        Returns:
            bool: True if exists, False otherwise
        """

    @abstractmethod
    def count(self) -> int:
        """
        Count total number of demand analyses.

        Returns:
            int: Total count
        """
