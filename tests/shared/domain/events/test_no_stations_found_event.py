"""Tests for No Stations Found Event."""

# pylint: disable=redefined-outer-name

from dataclasses import FrozenInstanceError
from unittest.mock import MagicMock
import pytest

from src.shared.domain.events import NoStationsFoundEvent
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
    event = NoStationsFoundEvent(postal_code=mock_postal_code)

    assert event.postal_code == mock_postal_code
    assert event.event_id is not None
    assert event.occurred_at is not None


def test_immutability(mock_postal_code):
    """
    Test that attributes cannot be changed after creation.
    """
    event = NoStationsFoundEvent(postal_code=mock_postal_code)

    with pytest.raises(FrozenInstanceError):
        event.postal_code = MagicMock()


def test_event_type_name(mock_postal_code):
    """
    Test that the event type name is correct.
    """
    event = NoStationsFoundEvent(postal_code=mock_postal_code)

    assert event.event_type() == "NoStationsFoundEvent"


def test_different_instances_have_unique_ids(mock_postal_code):
    """
    Test that each event instance gets a unique event_id.
    """
    event1 = NoStationsFoundEvent(postal_code=mock_postal_code)
    event2 = NoStationsFoundEvent(postal_code=mock_postal_code)

    assert event1.event_id != event2.event_id


def test_postal_code_captured_correctly():
    """
    Test that different postal codes are captured correctly.
    """
    postal_codes = ["10115", "10117", "10178", "12345"]

    for code in postal_codes:
        mock_pc = MagicMock(spec=PostalCode)
        mock_pc.value = code
        event = NoStationsFoundEvent(postal_code=mock_pc)
        assert event.postal_code.value == code
