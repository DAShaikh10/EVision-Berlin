from dataclasses import dataclass

from src.shared.domain.events import DomainEvent


@dataclass(frozen=True)
class DemandAnalysisCalculatedEvent(DomainEvent):
    """
    Emitted when: Demand analysis calculation is completed.
    Emitted by: DemandAnalysisService (Application Layer).
    Consumed by: UI (display analysis), Report generator.
    """

    postal_code: str
    population: int
    station_count: int
    demand_priority: str  # "High", "Medium", "Low"
    residents_per_station: float

    @staticmethod
    def log_demand_calculation(event: "DemandAnalysisCalculatedEvent"):
        print(
            f"[EVENT] - DemandAnalysisCalculatedEvent - Demand analysis calculated for postal code: {event.postal_code}"
        )
