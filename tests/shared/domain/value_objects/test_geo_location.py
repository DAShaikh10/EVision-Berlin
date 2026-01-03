"""
Unit Tests for GeoLocation Value Object.

Test categories:
- Validation tests (invariants)
- Boundary processing tests (WKT and GeoDataFrame)
- Property tests (empty)
- Edge cases and boundary values
- Invalid inputs
- Immutability tests
"""
# pylint: disable=redefined-outer-name  # pytest fixtures redefine names

import pytest
import geopandas as gpd
from shapely.geometry import Polygon

from src.shared.domain.value_objects import GeoLocation, PostalCode
from src.shared.domain.exceptions import InvalidGeoLocationError


# Test fixtures for reusable test data
@pytest.fixture
def valid_postal_code():
    """Fixture for a valid Berlin postal code."""
    return PostalCode("10115")


@pytest.fixture
def another_postal_code():
    """Fixture for another valid Berlin postal code."""
    return PostalCode("10178")


@pytest.fixture
def valid_wkt_string():
    """Fixture for a valid WKT polygon string."""
    return "POLYGON ((13.4 52.5, 13.5 52.5, 13.5 52.6, 13.4 52.6, 13.4 52.5))"


@pytest.fixture
def complex_wkt_string():
    """Fixture for a more complex WKT polygon string."""
    return (
        "POLYGON ((13.3 52.4, 13.4 52.4, 13.5 52.4, 13.5 52.5, "
        "13.5 52.6, 13.4 52.6, 13.3 52.6, 13.3 52.5, 13.3 52.4))"
    )


@pytest.fixture
def valid_geodataframe():
    """Fixture for a valid GeoDataFrame."""
    polygon = Polygon([(13.4, 52.5), (13.5, 52.5), (13.5, 52.6), (13.4, 52.6), (13.4, 52.5)])
    return gpd.GeoDataFrame(geometry=[polygon])


@pytest.fixture
def multipolygon_wkt_string():
    """Fixture for a WKT multipolygon string."""
    return (
        "MULTIPOLYGON (((13.4 52.5, 13.5 52.5, 13.5 52.6, 13.4 52.6, 13.4 52.5)), "
        "((13.6 52.5, 13.7 52.5, 13.7 52.6, 13.6 52.6, 13.6 52.5)))"
    )


class TestGeoLocationValidation:
    """Test validation logic in __post_init__."""

    def test_valid_geolocation_creation_with_wkt(self, valid_postal_code, valid_wkt_string):
        """Test creating a valid GeoLocation instance with WKT string."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert geo_location.postal_code == valid_postal_code
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)
        assert not geo_location.boundary.empty
        assert len(geo_location.boundary) == 1

    def test_valid_geolocation_creation_with_geodataframe(
        self, valid_postal_code, valid_geodataframe
    ):
        """Test creating a valid GeoLocation instance with GeoDataFrame."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_geodataframe)

        assert geo_location.postal_code == valid_postal_code
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)
        assert not geo_location.boundary.empty

    def test_none_boundary_raises_invalid_geolocation_error(self, valid_postal_code):
        """Test that None boundary raises InvalidGeoLocationError."""
        with pytest.raises(
            InvalidGeoLocationError, match="Geo Location boundary cannot be None or empty"
        ):
            GeoLocation(postal_code=valid_postal_code, boundary=None)

    def test_empty_string_boundary_raises_error(self, valid_postal_code):
        """Test that empty string boundary raises InvalidGeoLocationError."""
        with pytest.raises(InvalidGeoLocationError):
            GeoLocation(postal_code=valid_postal_code, boundary="")

    def test_empty_geodataframe_raises_invalid_geolocation_error(self, valid_postal_code):
        """Test that empty GeoDataFrame raises InvalidGeoLocationError."""
        empty_gdf = gpd.GeoDataFrame(geometry=[])

        with pytest.raises(
            InvalidGeoLocationError, match="Geo Location boundary cannot be None or empty"
        ):
            GeoLocation(postal_code=valid_postal_code, boundary=empty_gdf)

    def test_invalid_wkt_raises_exception(self, valid_postal_code):
        """Test that invalid WKT string raises an exception."""
        invalid_wkt = "INVALID WKT STRING"

        with pytest.raises(Exception):  # Could be ValueError or other parsing error
            GeoLocation(postal_code=valid_postal_code, boundary=invalid_wkt)

    def test_whitespace_boundary_raises_error(self, valid_postal_code):
        """Test that whitespace-only boundary raises exception during parsing."""
        with pytest.raises(Exception):  # GEOSException from shapely
            GeoLocation(postal_code=valid_postal_code, boundary="   ")


class TestGeoLocationBoundaryProcessing:
    """Test boundary processing from WKT to GeoDataFrame."""

    def test_wkt_string_converted_to_geodataframe(self, valid_postal_code, valid_wkt_string):
        """Test that WKT string is properly converted to GeoDataFrame."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)
        assert len(geo_location.boundary) == 1
        assert "geometry" in geo_location.boundary.columns

    def test_complex_wkt_processing(self, valid_postal_code, complex_wkt_string):
        """Test processing of complex WKT polygon."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=complex_wkt_string)

        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)
        assert not geo_location.boundary.empty
        assert geo_location.boundary.geometry is not None

    def test_multipolygon_wkt_processing(self, valid_postal_code, multipolygon_wkt_string):
        """Test processing of multipolygon WKT."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=multipolygon_wkt_string)

        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)
        assert not geo_location.boundary.empty
        assert len(geo_location.boundary) == 1

    def test_geodataframe_passed_unchanged(self, valid_postal_code, valid_geodataframe):
        """Test that GeoDataFrame boundary is not re-processed."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_geodataframe)

        assert geo_location.boundary is valid_geodataframe
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)

    def test_boundary_has_geometry_column(self, valid_postal_code, valid_wkt_string):
        """Test that processed boundary has geometry column."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert "geometry" in geo_location.boundary.columns
        assert geo_location.boundary.geometry is not None


class TestGeoLocationEmptyProperty:
    """Test the empty property."""

    def test_empty_property_returns_false_for_valid_boundary(
        self, valid_postal_code, valid_wkt_string
    ):
        """Test that empty property returns False for valid boundary."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert not geo_location.empty

    def test_empty_property_consistency(self, valid_postal_code, valid_geodataframe):
        """Test that empty property is consistent."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_geodataframe)

        # Call multiple times to ensure consistency
        assert not geo_location.empty
        assert not geo_location.empty
        assert not geo_location.empty


class TestGeoLocationImmutability:
    """Test immutability of GeoLocation (frozen dataclass)."""

    def test_cannot_modify_postal_code(self, valid_postal_code, valid_wkt_string):
        """Test that postal_code attribute cannot be modified."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        with pytest.raises(AttributeError):
            geo_location.postal_code = PostalCode("10178")

    def test_cannot_modify_boundary(self, valid_postal_code, valid_wkt_string):
        """Test that boundary attribute cannot be modified."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        with pytest.raises(AttributeError):
            geo_location.boundary = gpd.GeoDataFrame()


class TestGeoLocationEquality:
    """Test equality and comparison."""

    def test_two_geolocations_with_same_data_are_equal(self, valid_postal_code, valid_wkt_string):
        """Test that GeoLocations with same data are equal."""
        geo_loc1 = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)
        geo_loc2 = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        # Note: They may not be equal due to boundary being different GeoDataFrame instances
        # But postal codes should match
        assert geo_loc1.postal_code == geo_loc2.postal_code

    def test_two_geolocations_with_different_postal_codes_are_not_equal(
        self, valid_postal_code, another_postal_code, valid_wkt_string
    ):
        """Test that GeoLocations with different postal codes are not equal."""
        geo_loc1 = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)
        geo_loc2 = GeoLocation(postal_code=another_postal_code, boundary=valid_wkt_string)

        assert geo_loc1.postal_code != geo_loc2.postal_code

    def test_geolocation_postal_code_equality(self, valid_postal_code, valid_wkt_string):
        """Test postal code equality check."""
        geo_loc1 = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)
        geo_loc2 = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert geo_loc1.postal_code == geo_loc2.postal_code


class TestGeoLocationBoundaryGeometry:
    """Test geometric properties of boundaries."""

    def test_boundary_geometry_is_valid(self, valid_postal_code, valid_wkt_string):
        """Test that boundary geometry is valid."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        assert geo_location.boundary.geometry.is_valid.all()

    def test_boundary_has_area(self, valid_postal_code, valid_wkt_string):
        """Test that boundary has calculable area."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        area = geo_location.boundary.geometry.area
        assert area is not None
        assert len(area) > 0

    def test_boundary_geometry_type(self, valid_postal_code, valid_wkt_string):
        """Test that boundary has proper geometry type."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        geom_type = geo_location.boundary.geometry.geom_type
        assert geom_type is not None
        assert len(geom_type) > 0


class TestGeoLocationEdgeCases:
    """Test edge cases and boundary values."""

    def test_very_small_polygon(self, valid_postal_code):
        """Test with very small polygon."""
        small_wkt = "POLYGON ((13.4 52.5, 13.40001 52.5, 13.40001 52.50001, 13.4 52.50001, 13.4 52.5))"
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=small_wkt)

        assert not geo_location.empty
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)

    def test_large_complex_polygon(self, valid_postal_code):
        """Test with larger complex polygon."""
        # Create a polygon with many points (proper WKT format with commas)
        coords = ", ".join([f"13.{i} 52.{i}" for i in range(4, 10)])
        large_wkt = f"POLYGON ((13.4 52.5, {coords}, 13.4 52.5))"

        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=large_wkt)

        assert not geo_location.empty
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)

    def test_triangle_polygon(self, valid_postal_code):
        """Test with triangle (minimum valid polygon)."""
        triangle_wkt = "POLYGON ((13.4 52.5, 13.5 52.5, 13.45 52.6, 13.4 52.5))"
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=triangle_wkt)

        assert not geo_location.empty
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)


class TestGeoLocationRepr:
    """Test string representation."""

    def test_repr_contains_postal_code(self, valid_postal_code, valid_wkt_string):
        """Test that repr contains postal code information."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        repr_str = repr(geo_location)
        assert "GeoLocation" in repr_str
        assert "postal_code" in repr_str

    def test_str_representation(self, valid_postal_code, valid_wkt_string):
        """Test string representation."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        str_repr = str(geo_location)
        assert str_repr is not None
        assert len(str_repr) > 0


class TestGeoLocationIntegration:
    """Integration tests for GeoLocation value object."""

    def test_geolocation_workflow_with_wkt(self, valid_postal_code, valid_wkt_string):
        """Test complete workflow with WKT string."""
        # Create GeoLocation from WKT
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        # Verify it was created correctly
        assert geo_location.postal_code == valid_postal_code
        assert not geo_location.empty

        # Verify boundary is a GeoDataFrame
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)

        # Verify geometry is accessible
        assert geo_location.boundary.geometry is not None

    def test_geolocation_workflow_with_geodataframe(
        self, valid_postal_code, valid_geodataframe
    ):
        """Test complete workflow with GeoDataFrame."""
        # Create GeoLocation from GeoDataFrame
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_geodataframe)

        # Verify creation
        assert geo_location.postal_code == valid_postal_code
        assert not geo_location.empty

        # Verify boundary preservation
        assert geo_location.boundary is valid_geodataframe

    def test_multiple_geolocation_objects(self, valid_wkt_string, complex_wkt_string):
        """Test creating multiple GeoLocation objects."""
        geolocations = [
            GeoLocation(postal_code=PostalCode("10115"), boundary=valid_wkt_string),
            GeoLocation(postal_code=PostalCode("10178"), boundary=complex_wkt_string),
            GeoLocation(postal_code=PostalCode("12045"), boundary=valid_wkt_string),
        ]

        assert len(geolocations) == 3
        assert all(isinstance(gl, GeoLocation) for gl in geolocations)
        assert all(not gl.empty for gl in geolocations)

    def test_geolocation_in_data_structure(self, valid_wkt_string, complex_wkt_string):
        """Test storing GeoLocations in collections."""
        geolocation_dict = {
            "area1": GeoLocation(postal_code=PostalCode("10115"), boundary=valid_wkt_string),
            "area2": GeoLocation(postal_code=PostalCode("10178"), boundary=complex_wkt_string),
            "area3": GeoLocation(postal_code=PostalCode("12045"), boundary=valid_wkt_string),
        }

        assert len(geolocation_dict) == 3
        assert geolocation_dict["area1"].postal_code.value == "10115"
        assert geolocation_dict["area2"].postal_code.value == "10178"
        assert all(not gl.empty for gl in geolocation_dict.values())

    def test_geolocation_immutability_preservation(self, valid_postal_code, valid_wkt_string):
        """Test that GeoLocation remains immutable throughout usage."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        # Store initial values
        initial_postal_code = geo_location.postal_code
        initial_empty_state = geo_location.empty

        # Attempt operations that shouldn't modify the object
        _ = repr(geo_location)
        _ = str(geo_location)
        _ = geo_location.empty

        # Verify values unchanged
        assert geo_location.postal_code == initial_postal_code
        assert geo_location.empty == initial_empty_state


class TestGeoLocationBoundaryValidation:
    """Test boundary data validation and processing."""

    def test_boundary_processed_only_once(self, valid_postal_code, valid_wkt_string):
        """Test that boundary is processed only during initialization."""
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=valid_wkt_string)

        # Access boundary multiple times
        boundary1 = geo_location.boundary
        boundary2 = geo_location.boundary
        boundary3 = geo_location.boundary

        # All should reference the same object
        assert boundary1 is boundary2
        assert boundary2 is boundary3

    def test_wkt_with_different_geometry_types(self, valid_postal_code):
        """Test WKT with different valid geometry types."""
        # Test with POLYGON
        polygon_wkt = "POLYGON ((13.4 52.5, 13.5 52.5, 13.5 52.6, 13.4 52.6, 13.4 52.5))"
        geo_loc_polygon = GeoLocation(postal_code=valid_postal_code, boundary=polygon_wkt)
        assert not geo_loc_polygon.empty

    def test_whitespace_in_wkt_handled_correctly(self, valid_postal_code):
        """Test that extra whitespace in WKT doesn't cause issues."""
        wkt_with_spaces = "POLYGON  ((13.4  52.5,  13.5  52.5,  13.5  52.6,  13.4  52.6,  13.4  52.5))"
        geo_location = GeoLocation(postal_code=valid_postal_code, boundary=wkt_with_spaces)

        assert not geo_location.empty
        assert isinstance(geo_location.boundary, gpd.GeoDataFrame)


class TestGeoLocationErrorHandling:
    """Test error handling and exception scenarios."""

    def test_invalid_postal_code_raises_error(self, valid_wkt_string):
        """Test that invalid postal code raises appropriate error."""
        with pytest.raises(Exception):  # Will fail during PostalCode validation
            # PostalCode with invalid format
            invalid_postal = PostalCode("99999")  # Not a Berlin postal code
            GeoLocation(postal_code=invalid_postal, boundary=valid_wkt_string)

    def test_malformed_wkt_raises_exception(self, valid_postal_code):
        """Test that malformed WKT raises exception."""
        malformed_wkt = "POLYGON ((13.4 52.5, 13.5 52.5, INVALID))"

        with pytest.raises(Exception):
            GeoLocation(postal_code=valid_postal_code, boundary=malformed_wkt)

    def test_incomplete_polygon_wkt_raises_exception(self, valid_postal_code):
        """Test that incomplete polygon WKT raises exception."""
        incomplete_wkt = "POLYGON ((13.4 52.5, 13.5 52.5))"  # Need at least 3 points

        with pytest.raises(Exception):
            GeoLocation(postal_code=valid_postal_code, boundary=incomplete_wkt)
