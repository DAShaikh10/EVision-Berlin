"""Tests for Station Search Failed Event."""

# pylint: disable=redefined-outer-name

from dataclasses import FrozenInstanceError
from unittest.mock import MagicMock
import pytest

from src.shared.domain.events import StationSearchFailedEvent
from src.shared.domain.value_objects import PostalCode


@pytest.fixture
def mock_postal_code():
    """
    Pytest fixture to provide a mock PostalCode.
    """
    mock = MagicMock(spec=PostalCode)
    mock.value = "10115"
    return mock


def test_initialization(mock_postal_code):
    """
    Test that the event is initialized correctly with required fields.
    """
    error_message = "Database connection failed"
    error_type = "ConnectionError"

    event = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message=error_message,
        error_type=error_type,
    )

    assert event.postal_code == mock_postal_code
    assert event.error_message == error_message
    assert event.error_type == error_type
    assert event.event_id is not None
    assert event.occurred_at is not None


def test_initialization_without_error_type(mock_postal_code):
    """
    Test initialization without optional error_type parameter.
    """
    error_message = "Unknown error occurred"

    event = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message=error_message,
    )

    assert event.postal_code == mock_postal_code
    assert event.error_message == error_message
    assert event.error_type is None


def test_immutability(mock_postal_code):
    """
    Test that attributes cannot be changed after creation.
    """
    event = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message="Test error",
        error_type="TestError",
    )

    with pytest.raises(FrozenInstanceError):
        event.postal_code = MagicMock()

    with pytest.raises(FrozenInstanceError):
        event.error_message = "New error message"

    with pytest.raises(FrozenInstanceError):
        event.error_type = "NewType"


def test_event_type_name(mock_postal_code):
    """
    Test that the event type name is correct.
    """
    event = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message="Test error",
    )

    assert event.event_type() == "StationSearchFailedEvent"


def test_different_instances_have_unique_ids(mock_postal_code):
    """
    Test that each event instance gets a unique event_id.
    """
    event1 = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message="Error 1",
    )

    event2 = StationSearchFailedEvent(
        postal_code=mock_postal_code,
        error_message="Error 2",
    )

    assert event1.event_id != event2.event_id


def test_error_message_captured_correctly(mock_postal_code):
    """
    Test that various error messages are captured correctly.
    """
    test_messages = [
        "Repository timeout",
        "Invalid data format",
        "Network error",
        "Permission denied",
    ]

    for message in test_messages:
        event = StationSearchFailedEvent(
            postal_code=mock_postal_code,
            error_message=message,
        )
        assert event.error_message == message


def test_error_type_variations(mock_postal_code):
    """
    Test that different error types are handled correctly.
    """
    error_types = ["ValueError", "ConnectionError", "TimeoutError", None]

    for error_type in error_types:
        event = StationSearchFailedEvent(
            postal_code=mock_postal_code,
            error_message="Test error",
            error_type=error_type,
        )
        assert event.error_type == error_type
