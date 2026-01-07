"""
Shared Domain Event - Station Search Failed Event
"""

from typing import Optional
from dataclasses import dataclass

from src.shared.domain.value_objects import PostalCode

from .domain_event import DomainEvent


@dataclass(frozen=True)
class StationSearchFailedEvent(DomainEvent):
    """
    Domain Event: Search for charging stations has failed.

    Emitted by: ChargingStationService (Application Layer)
    Consumed by:
        - StationSearchEventHandler (logging/error tracking)
        - Analytics service (failure tracking)
        - UI (display error messages)
        - Monitoring/alerting systems

    This event captures when a station search operation fails,
    allowing the system to properly handle and track failures.
    """

    postal_code: PostalCode
    error_message: str
    error_type: Optional[str] = None
