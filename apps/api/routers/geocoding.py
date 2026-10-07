"""
Geocoding & Location Resolution Router for Astrovision.
Exposes location search endpoints for global cities and Indian towns, and custom coordinate validation.
"""
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from apps.api.engines.geocoding_engine import GeocodingEngine

router = APIRouter(prefix="/api/v1/location", tags=["Geocoding & Location Search"])

class LocationSearchItem(BaseModel):
    place_name: str
    country: str
    latitude: float
    longitude: float
    timezone_str: str

class LocationValidateRequest(BaseModel):
    latitude: float = Field(description="Geographic latitude in degrees [-90.0, 90.0]")
    longitude: float = Field(description="Geographic longitude in degrees [-180.0, 180.0]")
    timezone_str: str = Field(description="Authoritative IANA timezone string e.g. 'Asia/Kolkata'")

class LocationValidateResponse(BaseModel):
    is_valid: bool
    latitude: float
    longitude: float
    timezone_str: str

@router.get("/search", response_model=List[LocationSearchItem])
def search_location(query: str = Query(..., min_length=1, description="Place name or country search query")):
    """Searches canonical location database for place name or country string."""
    results = GeocodingEngine.search_location(query)
    return results

@router.post("/validate", response_model=LocationValidateResponse)
def validate_custom_location(req: LocationValidateRequest):
    """Validates custom manual latitude, longitude, and IANA timezone string."""
    valid = GeocodingEngine.validate_coordinates_and_timezone(req.latitude, req.longitude, req.timezone_str)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid location parameters: lat={req.latitude}, lon={req.longitude}, tz={req.timezone_str}"
        )
    return LocationValidateResponse(
        is_valid=True,
        latitude=req.latitude,
        longitude=req.longitude,
        timezone_str=req.timezone_str
    )
