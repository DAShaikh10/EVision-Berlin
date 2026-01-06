"""
Shared Domain Enums Module.

Consolidated file containing all shared domain enumerations.
"""

from enum import Enum


class CapacityCategory(Enum):
    """
    Enumeration for capacity classification.

    Used to classify capacity values into standard categories.
    """

    NONE = "None"  # Zero capacity
    LOW = "Low"  # Below 33rd percentile
    MEDIUM = "Medium"  # Between 33rd and 66th percentile
    HIGH = "High"  # Above 66th percentile


class ChargingCategory(Enum):
    """
    Enumeration for charging station power categories.

    Used to classify charging stations based on their power output.
    """

    NORMAL = "NORMAL"  # < 50 kW (AC charging, home wallboxes)
    FAST = "FAST"  # 50-149 kW (DC fast charging)
    ULTRA = "ULTRA"  # >= 150 kW (Ultra-fast DC charging)


class CoverageAssessment(Enum):
    """
    Enumeration for demand-based coverage assessment levels.

    Used by DemandAnalysisAggregate to assess infrastructure adequacy
    based on population-to-station ratios.
    """

    CRITICAL = "CRITICAL"
    POOR = "POOR"
    ADEQUATE = "ADEQUATE"
    GOOD = "GOOD"


class CoverageLevel(Enum):
    """
    Enumeration for infrastructure coverage levels.

    Used by PostalCodeAreaAggregate to assess charging station coverage.
    """

    NO_COVERAGE = "NO_COVERAGE"
    POOR = "POOR"
    ADEQUATE = "ADEQUATE"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"


class PopulationDensityCategory(Enum):
    """
    Enumeration for population density categories.

    Used to classify areas based on population density for infrastructure planning.
    """

    LOW = "LOW"  # < 10,000 residents (low density/rural)
    MEDIUM = "MEDIUM"  # 10,000-20,000 residents (suburban/moderate density)
    HIGH = "HIGH"  # > 20,000 residents (dense urban area)

