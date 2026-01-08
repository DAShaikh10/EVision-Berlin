"""
Shared Domain Event - Postal Code Validated Event
"""

from dataclasses import dataclass

from src.shared.domain.value_objects import PostalCode

from .domain_event import DomainEvent


@dataclass(frozen=True)
class PostalCodeValidatedEvent(DomainEvent):
    """
    Domain Event: A postal code has been successfully validated.

    Emitted by: PostalCode value object (Domain Layer)
    Consumed by:
        - PostalCodeEventHandler (logging/auditing)
        - Analytics service (validation tracking)
        - Monitoring service (validation metrics)

    This event is emitted when a postal code passes all validation rules:
    - Format validation (5 digits, numeric)
    - Berlin region validation (starts with 10, 12, 13, or 14)
    - Range validation (within Berlin boundaries)

    This is a pure data class representing something that happened in the domain.
    Event handlers are in the application layer (event_handlers/).
    """

    postal_code: PostalCode
