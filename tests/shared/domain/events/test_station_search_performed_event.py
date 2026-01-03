import unittest
from unittest.mock import MagicMock

from src.shared.domain.events.StationSearchPerformedEvent import StationSearchPerformedEvent
from src.shared.domain.value_objects.PostalCode import PostalCode

class TestStationSearchPerformedEvent(unittest.TestCase):
    """
    Unit tests for the StationSearchPerformedEvent.
    """

    def setUp(self):
        self.mock_postal_code = MagicMock(spec=PostalCode)
        self.mock_postal_code.value = "10115"

    def test_initialization(self):
        """
        Test that the event is initialized correctly with required fields.
        """
        stations_count = 10
        
        event = StationSearchPerformedEvent(
            postal_code=self.mock_postal_code,
            stations_found=stations_count
        )

        self.assertEqual(event.postal_code, self.mock_postal_code)
        self.assertEqual(event.stations_found, stations_count)
        self.assertEqual(event.search_parameters, {}) # Default empty dict
        
        # Verify inherited fields
        self.assertIsNotNone(event.event_id)
        self.assertIsNotNone(event.occurred_at)

    def test_initialization_with_parameters(self):
        """
        Test initialization with optional search_parameters.
        """
        params = {"origin": self.mock_postal_code}
        
        event = StationSearchPerformedEvent(
            postal_code=self.mock_postal_code,
            stations_found=5,
            search_parameters=params
        )

        self.assertEqual(event.search_parameters, params)

    def test_immutability(self):
        """
        Test that attributes cannot be changed after creation.
        """
        event = StationSearchPerformedEvent(
            postal_code=self.mock_postal_code,
            stations_found=5
        )

        from dataclasses import FrozenInstanceError
        with self.assertRaises(FrozenInstanceError):
            event.stations_found = 0

    def test_event_type_name(self):
        """
        Test that the event type name is correct.
        """
        event = StationSearchPerformedEvent(
            postal_code=self.mock_postal_code,
            stations_found=5
        )
        self.assertEqual(event.event_type(), "StationSearchPerformedEvent")

if __name__ == '__main__':
    unittest.main()