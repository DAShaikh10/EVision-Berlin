"""
Unit Tests for PopulationData Value Object.

Test categories:
- Validation tests (invariants)
- Method tests (business logic)
- Immutability tests
- Edge cases and boundary values
- Integration tests
"""
# pylint: disable=redefined-outer-name  # pytest fixtures redefine names

import pytest

from src.shared.domain.value_objects import PopulationData, PostalCode


# Test fixtures for reusable test data
@pytest.fixture
def valid_postal_code():
    """Fixture for a valid Berlin postal code."""
    return PostalCode("10115")


@pytest.fixture
def another_postal_code():
    """Fixture for another valid Berlin postal code."""
    return PostalCode("12045")


class TestPopulationDataValidation:
    """Test validation logic in __post_init__."""

    def test_valid_population_data_creation(self, valid_postal_code):
        """Test creating a valid PopulationData instance."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        assert pop_data.postal_code == valid_postal_code
        assert pop_data.population == 30000

    def test_zero_population_is_valid(self, valid_postal_code):
        """Test that zero population is valid."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data.population == 0

    def test_large_population_is_valid(self, valid_postal_code):
        """Test with large population value."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=1000000)

        assert pop_data.population == 1000000

    def test_negative_population_raises_value_error(self, valid_postal_code):
        """Test that negative population raises ValueError."""
        with pytest.raises(ValueError, match="Population cannot be negative, got: -1000"):
            PopulationData(postal_code=valid_postal_code, population=-1000)

    def test_negative_one_population_raises_value_error(self, valid_postal_code):
        """Test that -1 population raises ValueError."""
        with pytest.raises(ValueError, match="Population cannot be negative, got: -1"):
            PopulationData(postal_code=valid_postal_code, population=-1)

    def test_population_with_different_postal_codes(self, valid_postal_code, another_postal_code):
        """Test creating population data with different postal codes."""
        pop_data1 = PopulationData(postal_code=valid_postal_code, population=25000)
        pop_data2 = PopulationData(postal_code=another_postal_code, population=18000)

        assert pop_data1.postal_code != pop_data2.postal_code
        assert pop_data1.population != pop_data2.population


class TestPopulationDataGetPopulation:
    """Test get_population query method."""

    def test_get_population_returns_correct_value(self, valid_postal_code):
        """Test that get_population returns the correct population value."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        assert pop_data.get_population() == 30000

    def test_get_population_with_zero(self, valid_postal_code):
        """Test get_population with zero population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data.get_population() == 0

    def test_get_population_with_large_value(self, valid_postal_code):
        """Test get_population with large population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=999999)

        assert pop_data.get_population() == 999999

    def test_get_population_consistency(self, valid_postal_code):
        """Test that get_population returns consistent values."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=25000)

        # Call multiple times to ensure consistency
        assert pop_data.get_population() == 25000
        assert pop_data.get_population() == 25000
        assert pop_data.get_population() == 25000


class TestPopulationDataDensityCategory:
    """Test get_population_density_category business logic."""

    def test_high_density_category_above_20000(self, valid_postal_code):
        """Test HIGH category for population > 20,000."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=25000)

        assert pop_data.get_population_density_category() == "HIGH"

    def test_high_density_at_boundary_20001(self, valid_postal_code):
        """Test HIGH category at boundary (20,001)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=20001)

        assert pop_data.get_population_density_category() == "HIGH"

    def test_medium_density_at_upper_boundary(self, valid_postal_code):
        """Test MEDIUM category at upper boundary (20,000)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=20000)

        assert pop_data.get_population_density_category() == "MEDIUM"

    def test_medium_density_in_range(self, valid_postal_code):
        """Test MEDIUM category in range (10,000-20,000)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=15000)

        assert pop_data.get_population_density_category() == "MEDIUM"

    def test_medium_density_at_lower_boundary(self, valid_postal_code):
        """Test MEDIUM category at lower boundary (10,001)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=10001)

        assert pop_data.get_population_density_category() == "MEDIUM"

    def test_low_density_at_boundary(self, valid_postal_code):
        """Test LOW category at boundary (10,000)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=10000)

        assert pop_data.get_population_density_category() == "LOW"

    def test_low_density_below_10000(self, valid_postal_code):
        """Test LOW category for population < 10,000."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=5000)

        assert pop_data.get_population_density_category() == "LOW"

    def test_low_density_with_zero_population(self, valid_postal_code):
        """Test LOW category with zero population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data.get_population_density_category() == "LOW"

    def test_low_density_with_one_person(self, valid_postal_code):
        """Test LOW category with minimal population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=1)

        assert pop_data.get_population_density_category() == "LOW"


class TestPopulationDataHighDensity:
    """Test is_high_density business rule."""

    def test_is_high_density_above_15000(self, valid_postal_code):
        """Test high density returns True for population > 15,000."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=20000)

        assert pop_data.is_high_density() is True

    def test_is_high_density_at_boundary_15001(self, valid_postal_code):
        """Test high density at boundary (15,001)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=15001)

        assert pop_data.is_high_density() is True

    def test_is_not_high_density_at_15000(self, valid_postal_code):
        """Test not high density at exactly 15,000."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=15000)

        assert pop_data.is_high_density() is False

    def test_is_not_high_density_below_15000(self, valid_postal_code):
        """Test not high density for population < 15,000."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=10000)

        assert pop_data.is_high_density() is False

    def test_is_not_high_density_zero(self, valid_postal_code):
        """Test not high density with zero population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data.is_high_density() is False

    def test_is_high_density_very_large_population(self, valid_postal_code):
        """Test high density with very large population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=100000)

        assert pop_data.is_high_density() is True


class TestPopulationDataDemandRatio:
    """Test calculate_demand_ratio business calculation."""

    def test_demand_ratio_with_stations(self, valid_postal_code):
        """Test demand ratio calculation with stations present."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        ratio = pop_data.calculate_demand_ratio(station_count=5)

        assert ratio == 6000.0

    def test_demand_ratio_with_one_station(self, valid_postal_code):
        """Test demand ratio with single station."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=15000)

        ratio = pop_data.calculate_demand_ratio(station_count=1)

        assert ratio == 15000.0

    def test_demand_ratio_with_zero_stations(self, valid_postal_code):
        """Test demand ratio with zero stations (returns population)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=25000)

        ratio = pop_data.calculate_demand_ratio(station_count=0)

        assert ratio == 25000.0

    def test_demand_ratio_with_more_stations_than_people(self, valid_postal_code):
        """Test demand ratio when stations outnumber population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=100)

        ratio = pop_data.calculate_demand_ratio(station_count=200)

        assert ratio == 0.5

    def test_demand_ratio_with_zero_population(self, valid_postal_code):
        """Test demand ratio with zero population."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        ratio = pop_data.calculate_demand_ratio(station_count=5)

        assert ratio == 0.0

    def test_demand_ratio_with_zero_population_and_zero_stations(self, valid_postal_code):
        """Test demand ratio with zero population and zero stations."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        ratio = pop_data.calculate_demand_ratio(station_count=0)

        assert ratio == 0.0

    def test_demand_ratio_fractional_result(self, valid_postal_code):
        """Test demand ratio with fractional result."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=10000)

        ratio = pop_data.calculate_demand_ratio(station_count=3)

        assert ratio == pytest.approx(3333.33, rel=0.01)

    def test_demand_ratio_consistency(self, valid_postal_code):
        """Test that demand ratio calculation is consistent."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        # Calculate multiple times with same input
        ratio1 = pop_data.calculate_demand_ratio(station_count=5)
        ratio2 = pop_data.calculate_demand_ratio(station_count=5)
        ratio3 = pop_data.calculate_demand_ratio(station_count=5)

        assert ratio1 == ratio2 == ratio3 == 6000.0


class TestPopulationDataImmutability:
    """Test immutability of PopulationData (frozen dataclass)."""

    def test_cannot_modify_postal_code(self, valid_postal_code):
        """Test that postal_code attribute cannot be modified."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        with pytest.raises(AttributeError):
            pop_data.postal_code = PostalCode("12045")

    def test_cannot_modify_population(self, valid_postal_code):
        """Test that population attribute cannot be modified."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        with pytest.raises(AttributeError):
            pop_data.population = 50000


class TestPopulationDataEquality:
    """Test equality and comparison."""

    def test_two_population_data_with_same_values_are_equal(self, valid_postal_code):
        """Test that PopulationData with same values are equal."""
        pop_data1 = PopulationData(postal_code=valid_postal_code, population=30000)
        pop_data2 = PopulationData(postal_code=valid_postal_code, population=30000)

        assert pop_data1 == pop_data2

    def test_two_population_data_with_different_population_are_not_equal(self, valid_postal_code):
        """Test that PopulationData with different population are not equal."""
        pop_data1 = PopulationData(postal_code=valid_postal_code, population=30000)
        pop_data2 = PopulationData(postal_code=valid_postal_code, population=25000)

        assert pop_data1 != pop_data2

    def test_two_population_data_with_different_postal_codes_are_not_equal(
        self, valid_postal_code, another_postal_code
    ):
        """Test that PopulationData with different postal codes are not equal."""
        pop_data1 = PopulationData(postal_code=valid_postal_code, population=30000)
        pop_data2 = PopulationData(postal_code=another_postal_code, population=30000)

        assert pop_data1 != pop_data2

    def test_population_data_equality_with_zero(self, valid_postal_code):
        """Test equality with zero population."""
        pop_data1 = PopulationData(postal_code=valid_postal_code, population=0)
        pop_data2 = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data1 == pop_data2


class TestPopulationDataRepr:
    """Test string representation."""

    def test_repr_contains_postal_code_and_population(self, valid_postal_code):
        """Test that repr contains postal code and population information."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        repr_str = repr(pop_data)
        assert "PopulationData" in repr_str
        assert "postal_code" in repr_str
        assert "population" in repr_str

    def test_str_representation(self, valid_postal_code):
        """Test string representation."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        str_repr = str(pop_data)
        assert str_repr is not None
        assert len(str_repr) > 0


class TestPopulationDataEdgeCases:
    """Test edge cases and boundary values."""

    def test_minimum_valid_population(self, valid_postal_code):
        """Test minimum valid population (zero)."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=0)

        assert pop_data.population == 0
        assert pop_data.get_population() == 0
        assert pop_data.get_population_density_category() == "LOW"
        assert not pop_data.is_high_density()

    def test_population_one(self, valid_postal_code):
        """Test population of one."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=1)

        assert pop_data.population == 1
        assert pop_data.get_population() == 1

    def test_very_large_population(self, valid_postal_code):
        """Test with very large population value."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=10000000)

        assert pop_data.population == 10000000
        assert pop_data.get_population() == 10000000
        assert pop_data.get_population_density_category() == "HIGH"
        assert pop_data.is_high_density()

    def test_density_boundary_values(self, valid_postal_code):
        """Test all density category boundaries."""
        # Just below HIGH threshold
        pop_data_20000 = PopulationData(postal_code=valid_postal_code, population=20000)
        assert pop_data_20000.get_population_density_category() == "MEDIUM"

        # Just above HIGH threshold
        pop_data_20001 = PopulationData(postal_code=valid_postal_code, population=20001)
        assert pop_data_20001.get_population_density_category() == "HIGH"

        # Just below MEDIUM threshold
        pop_data_10000 = PopulationData(postal_code=valid_postal_code, population=10000)
        assert pop_data_10000.get_population_density_category() == "LOW"

        # Just above MEDIUM threshold
        pop_data_10001 = PopulationData(postal_code=valid_postal_code, population=10001)
        assert pop_data_10001.get_population_density_category() == "MEDIUM"


class TestPopulationDataIntegration:
    """Integration tests for PopulationData value object."""

    def test_population_data_complete_workflow(self, valid_postal_code):
        """Test complete workflow with PopulationData."""
        # Create population data
        pop_data = PopulationData(postal_code=valid_postal_code, population=25000)

        # Verify creation
        assert pop_data.postal_code == valid_postal_code
        assert pop_data.population == 25000

        # Test query method
        assert pop_data.get_population() == 25000

        # Test business logic methods
        assert pop_data.get_population_density_category() == "HIGH"
        assert pop_data.is_high_density() is True

        # Test calculation method
        ratio = pop_data.calculate_demand_ratio(station_count=5)
        assert ratio == 5000.0

    def test_multiple_population_data_objects(self):
        """Test creating multiple PopulationData objects."""
        pop_data_list = [
            PopulationData(postal_code=PostalCode("10115"), population=30000),
            PopulationData(postal_code=PostalCode("10178"), population=15000),
            PopulationData(postal_code=PostalCode("12045"), population=8000),
        ]

        assert len(pop_data_list) == 3
        assert all(isinstance(pd, PopulationData) for pd in pop_data_list)
        assert sum(pd.get_population() for pd in pop_data_list) == 53000

    def test_population_data_in_data_structure(self):
        """Test storing PopulationData in collections."""
        population_dict = {
            "area1": PopulationData(postal_code=PostalCode("10115"), population=30000),
            "area2": PopulationData(postal_code=PostalCode("10178"), population=18000),
            "area3": PopulationData(postal_code=PostalCode("12045"), population=12000),
        }

        assert len(population_dict) == 3
        assert population_dict["area1"].get_population() == 30000
        assert population_dict["area2"].postal_code.value == "10178"
        assert all(pd.get_population() > 0 for pd in population_dict.values())

    def test_population_data_immutability_throughout_usage(self, valid_postal_code):
        """Test that PopulationData remains immutable throughout usage."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=25000)

        # Store initial values
        initial_postal_code = pop_data.postal_code
        initial_population = pop_data.population

        # Perform various operations
        _ = pop_data.get_population()
        _ = pop_data.get_population_density_category()
        _ = pop_data.is_high_density()
        _ = pop_data.calculate_demand_ratio(5)

        # Verify values unchanged
        assert pop_data.postal_code == initial_postal_code
        assert pop_data.population == initial_population

    def test_high_density_correlation_with_category(self, valid_postal_code):
        """Test correlation between is_high_density and density category."""
        # Population at 16000 should be high density but MEDIUM category
        pop_data = PopulationData(postal_code=valid_postal_code, population=16000)

        # High density (> 15000) but MEDIUM category (10000-20000)
        assert pop_data.is_high_density() is True
        assert pop_data.get_population_density_category() == "MEDIUM"

    def test_demand_ratio_with_different_scenarios(self, valid_postal_code):
        """Test demand ratio calculation in various scenarios."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=30000)

        # Different station counts
        scenarios = [
            (1, 30000.0),
            (2, 15000.0),
            (5, 6000.0),
            (10, 3000.0),
            (0, 30000.0),  # Zero stations returns population
        ]

        for station_count, expected_ratio in scenarios:
            ratio = pop_data.calculate_demand_ratio(station_count)
            assert ratio == expected_ratio

    def test_consistency_across_method_calls(self, valid_postal_code):
        """Test that all methods return consistent results across multiple calls."""
        pop_data = PopulationData(postal_code=valid_postal_code, population=18000)

        # Call each method multiple times
        populations = [pop_data.get_population() for _ in range(3)]
        categories = [pop_data.get_population_density_category() for _ in range(3)]
        densities = [pop_data.is_high_density() for _ in range(3)]
        ratios = [pop_data.calculate_demand_ratio(6) for _ in range(3)]

        # All calls should return same values
        assert len(set(populations)) == 1
        assert len(set(categories)) == 1
        assert len(set(densities)) == 1
        assert len(set(ratios)) == 1
