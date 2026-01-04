"""
Shared pytest fixtures for tests.
"""

from unittest.mock import Mock

import pytest

from src.shared.domain.entities import ChargingStation
from src.shared.domain.value_objects import PostalCode


@pytest.fixture
def valid_postal_code():
    """Provide a valid Berlin postal code for tests."""
    return PostalCode("10115")


@pytest.fixture
def mock_charging_station():
    """Create a mock charging station with common attributes."""
    station = Mock(spec=ChargingStation)
    station.postal_code = "10115"
    station.latitude = 52.5200
    station.longitude = 13.4050

    power_capacity_mock = Mock()
    power_capacity_mock.kilowatts = 50.0
    station.power_capacity = power_capacity_mock

    station.is_fast_charger = Mock(return_value=True)
    station.get_charging_category = Mock(return_value="FAST")
    return station


@pytest.fixture
def mock_slow_station():
    """Create a mock slow charging station (<50kW)."""
    station = Mock(spec=ChargingStation)
    station.postal_code = "10115"

    power_capacity_mock = Mock()
    power_capacity_mock.kilowatts = 22.0
    station.power_capacity = power_capacity_mock

    station.is_fast_charger = Mock(return_value=False)
    station.get_charging_category = Mock(return_value="NORMAL")
    return station
