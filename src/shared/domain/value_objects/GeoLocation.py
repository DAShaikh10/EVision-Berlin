"""
GeoLocation Value Object Module.
"""

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING
import logging

import geopandas as gpd

from src.shared.domain.exceptions import InvalidGeoLocationError

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.shared.domain.value_objects.PostalCode import PostalCode


def _process_boundary(boundary_wkt: str) -> gpd.GeoDataFrame:
    """
    Process WKT boundary string into a GeoDataFrame.
    
    Args:
        boundary_wkt: WKT string representation of the boundary geometry
        
    Returns:
        GeoDataFrame with the boundary geometry
    """
    logger.info(f"_process_boundary called with WKT length: {len(boundary_wkt) if boundary_wkt else 0}")
    if not boundary_wkt:
        logger.warning("Empty boundary_wkt provided")
        return None
    try:
        gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_wkt([boundary_wkt]))
        logger.info(f"✓ Successfully created GeoDataFrame with shape: {gdf.shape}")
        return gdf
    except Exception as e:
        logger.error(f"Error processing boundary WKT: {e}", exc_info=True)
        raise


@dataclass(frozen=True)
class GeoLocation:
    """
    Entity: Represents geographic location data.

    This entity encapsulates geographic information such as coordinates and boundaries.
    """

    postal_code: 'PostalCode'
    boundary: Any = field(default=None, repr=False)

    def __post_init__(self):
        """
        Process and validate the boundary data on creation.
        """
        logger.info(f"GeoLocation __post_init__ called for postal_code: {self.postal_code}")
        logger.info(f"Initial boundary type: {type(self.boundary)}")
        logger.info(f"Initial boundary value (first 200 chars): {str(self.boundary)[:200] if self.boundary else 'None'}")
        
        # Process the boundary if it's a WKT string
        if isinstance(self.boundary, str):
            logger.info("Boundary is a string, processing WKT...")
            processed_boundary = _process_boundary(self.boundary)
            logger.info(f"Processed boundary type: {type(processed_boundary)}")
            if processed_boundary is not None:
                logger.info(f"Processed boundary shape: {processed_boundary.shape}")
                logger.info(f"Processed boundary columns: {processed_boundary.columns.tolist()}")
            # Use object.__setattr__ because the dataclass is frozen
            object.__setattr__(self, 'boundary', processed_boundary)
        
        # Validate
        if self.boundary is None or (isinstance(self.boundary, gpd.GeoDataFrame) and self.boundary.empty):
            logger.error(f"GeoLocation validation failed - boundary is None or empty")
            raise InvalidGeoLocationError("Geo Location boundary cannot be None or empty.")
        
        logger.info(f"✓ GeoLocation created successfully for {self.postal_code}")
    
    @property
    def empty(self) -> bool:
        """
        Check if the GeoLocation has an empty boundary.
        
        Returns:
            True if boundary is None or empty, False otherwise
        """
        return self.boundary is None or (isinstance(self.boundary, gpd.GeoDataFrame) and self.boundary.empty)
