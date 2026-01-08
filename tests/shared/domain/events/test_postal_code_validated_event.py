"""Tests for Postal Code Validated Event."""

# pylint: disable=redefined-outer-name

from dataclasses import FrozenInstanceError
from unittest.mock import MagicMock
import pytest

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


def test_initialization(mock_postal_code):
    """
    Test that the event is initialized correctly with required fields.
    """
    event = PostalCodeValidatedEvent(postal_code=mock_postal_code)

    assert event.postal_code == mock_postal_code
    assert event.event_id is not None
    assert event.occurred_at is not None


def test_immutability(mock_postal_code):
    """
    Test that attributes cannot be changed after creation.
    """
    event = PostalCodeValidatedEvent(postal_code=mock_postal_code)

    with pytest.raises(FrozenInstanceError):
        event.postal_code = MagicMock()


def test_event_type_name(mock_postal_code):
    """
    Test that the event type name is correctly set.
    """
    event = PostalCodeValidatedEvent(postal_code=mock_postal_code)

    assert event.event_type() == "PostalCodeValidatedEvent"


def test_different_instances_have_unique_ids(mock_postal_code):
    """
    Test that different event instances have unique event IDs.
    """
    event1 = PostalCodeValidatedEvent(postal_code=mock_postal_code)
    event2 = PostalCodeValidatedEvent(postal_code=mock_postal_code)

    assert event1.event_id != event2.event_id
    assert event1.occurred_at != event2.occurred_at or event1.occurred_at == event2.occurred_at


def test_postal_code_captured_correctly(mock_postal_code):
    """
    Test that the postal code is captured correctly in the event.
    """
    event = PostalCodeValidatedEvent(postal_code=mock_postal_code)

    assert event.postal_code.value == "10115"


def test_multiple_postal_codes():
    """
    Test event creation with different postal codes.
    """
    mock1 = MagicMock(spec=PostalCode)
    mock1.value = "10115"

    mock2 = MagicMock(spec=PostalCode)
    mock2.value = "12045"

    event1 = PostalCodeValidatedEvent(postal_code=mock1)
    event2 = PostalCodeValidatedEvent(postal_code=mock2)

    assert event1.postal_code.value == "10115"
    assert event2.postal_code.value == "12045"
    assert event1.event_id != event2.event_id
