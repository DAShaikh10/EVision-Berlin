"""
Shared Domain Event - No Stations Found Event
"""

from dataclasses import dataclass

from src.shared.domain.value_objects import PostalCode

from .domain_event import DomainEvent


@dataclass(frozen=True)
class NoStationsFoundEvent(DomainEvent):
    """
    Domain Event: Search completed successfully but found no stations.

    Emitted by: ChargingStationService (Application Layer)
    Consumed by:
        - StationSearchEventHandler (logging/tracking)
        - Analytics service (coverage gap identification)
        - UI (display appropriate messages)
        - Planning systems (infrastructure gap analysis)

    This event represents a successful search operation that found zero stations,
    which is useful for identifying areas with no charging infrastructure.
    """

    postal_code: PostalCode
