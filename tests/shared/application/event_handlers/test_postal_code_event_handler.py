"""Tests for Postal Code Event Handler."""

# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock, patch
import pytest

from src.shared.application.event_handlers import PostalCodeEventHandler
from src.shared.domain.events import PostalCodeValidatedEvent
from src.shared.domain.value_objects import PostalCode


@pytest.fixture
def mock_postal_code():
    """
    Pytest fixture to provide a mock PostalCode.
    """
    mock = MagicMock(spec=PostalCode)
    mock.value = "10115"
    return mock


@pytest.fixture
def postal_code_validated_event(mock_postal_code):
    """
    Pytest fixture to provide a PostalCodeValidatedEvent.
    """
    return PostalCodeValidatedEvent(postal_code=mock_postal_code)


class TestPostalCodeEventHandlerInitialization:
    """
    Test PostalCodeEventHandler initialization.
    """

    def test_handler_can_be_instantiated(self):
        """
        Test that PostalCodeEventHandler can be instantiated.
        """
        handler = PostalCodeEventHandler()
        assert handler is not None


class TestHandlePostalCodeValidated:
    """
    Test handle_postal_code_validated method.
    """

    @patch("src.shared.application.event_handlers.postal_code_event_handler.logger")
    def test_logs_postal_code_validated_event(self, mock_logger, postal_code_validated_event):
        """
        Test that the handler logs the postal code validated event.
        """
        PostalCodeEventHandler.handle_postal_code_validated(postal_code_validated_event)

        mock_logger.info.assert_called_once_with(
            "[EVENT] Postal code validated successfully: %s",
            "10115",
        )

    @patch("src.shared.application.event_handlers.postal_code_event_handler.logger")
    def test_handles_different_postal_codes(self, mock_logger):
        """
        Test that the handler correctly logs different postal codes.
        """
        mock1 = MagicMock(spec=PostalCode)
        mock1.value = "12045"
        event1 = PostalCodeValidatedEvent(postal_code=mock1)

        mock2 = MagicMock(spec=PostalCode)
        mock2.value = "13055"
        event2 = PostalCodeValidatedEvent(postal_code=mock2)

        PostalCodeEventHandler.handle_postal_code_validated(event1)
        PostalCodeEventHandler.handle_postal_code_validated(event2)

        assert mock_logger.info.call_count == 2
        first_call = mock_logger.info.call_args_list[0]
        second_call = mock_logger.info.call_args_list[1]

        assert "12045" in str(first_call)
        assert "13055" in str(second_call)

    @patch("src.shared.application.event_handlers.postal_code_event_handler.logger")
    def test_is_static_method(self, mock_logger, postal_code_validated_event):
        """
        Test that handle_postal_code_validated is a static method.
        """
        # Should work without instantiating the class
        PostalCodeEventHandler.handle_postal_code_validated(postal_code_validated_event)

        mock_logger.info.assert_called_once()


class TestPostalCodeEventHandlerIntegration:
    """
    Integration tests for PostalCodeEventHandler.
    """

    @patch("src.shared.application.event_handlers.postal_code_event_handler.logger")
    def test_handles_multiple_events_in_sequence(self, mock_logger):
        """
        Test that the handler can process multiple events in sequence.
        """
        postal_codes = ["10115", "12045", "13055", "14050"]
        events = []

        for code in postal_codes:
            mock = MagicMock(spec=PostalCode)
            mock.value = code
            events.append(PostalCodeValidatedEvent(postal_code=mock))

        for event in events:
            PostalCodeEventHandler.handle_postal_code_validated(event)

        assert mock_logger.info.call_count == len(postal_codes)

        # Verify all postal codes were logged
        for i, code in enumerate(postal_codes):
            call_args = mock_logger.info.call_args_list[i]
            assert code in str(call_args)
