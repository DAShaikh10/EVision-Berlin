"""
Shared Application Event Handler - Postal Code Events.
"""

from src.shared.infrastructure import get_logger

from src.shared.domain.events import PostalCodeValidatedEvent

logger = get_logger(__name__)


class PostalCodeEventHandler:
    """
    Handler for postal code validation events.

    Responsibilities:
    - Log postal code validations for auditing
    - Track validation metrics for monitoring
    - Support analytics on postal code usage patterns
    """

    @staticmethod
    def handle_postal_code_validated(event: PostalCodeValidatedEvent) -> None:
        """
        Handle postal code validated event.

        Args:
            event: The PostalCodeValidatedEvent instance.
        """
        logger.info(
            "[EVENT] Postal code validated successfully: %s",
            event.postal_code.value,
        )
