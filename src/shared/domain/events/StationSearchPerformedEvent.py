from typing import Dict
from dataclasses import dataclass, field

from .DomainEvent import DomainEvent
from src.shared.domain.value_objects import PostalCode


@dataclass(frozen=True)
class StationSearchPerformedEvent(DomainEvent):
    """
    Emitted when: Search for charging stations is performed.
    Emitted by: StationSearchService (Application Layer).
    Consumed by: UI (display results), Analytics (track usage).
    """

    postal_code: PostalCode
    stations_found: int
    search_parameters: Dict[str, PostalCode] = field(default_factory=dict)

    @staticmethod
    def log_station_search(event: "StationSearchPerformedEvent"):
        print(
            f"[EVENT] - StationSearchPerformedEvent - Station search performed for postal code: {event.postal_code.value}"
        )
