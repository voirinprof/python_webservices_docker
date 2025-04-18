from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Initialize FastAPI application
app = FastAPI(title="GeoJSON Points API",
    description="API for managing and filtering geographic points in GeoJSON format.",
    version="1.0.0",
    openapi_version="3.1.0")

# Static data: list of points with attributes
POINTS = [
    {"name": "Point_A", "value": 50, "coordinates": [-73.935, 40.730]},
    {"name": "Point_B", "value": 75, "coordinates": [2.352, 48.856]},
    {"name": "Point_C", "value": 20, "coordinates": [-0.127, 51.507]},
    {"name": "Point_D", "value": 90, "coordinates": [139.691, 35.689]},
    {"name": "Point_E", "value": 30, "coordinates": [151.209, -33.868]}
]

# Pydantic models for validation and documentation
class GeoJSONGeometry(BaseModel):
    type: str
    coordinates: List[float]

class GeoJSONProperties(BaseModel):
    name: str
    value: int

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJSONGeometry
    properties: GeoJSONProperties

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]

class FilterCriteria(BaseModel):
    min_value: Optional[int] = None
    name_contains: Optional[str] = None

def to_geojson_feature(point: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a point to a GeoJSON Feature."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": point["coordinates"]
        },
        "properties": {
            "name": point["name"],
            "value": point["value"]
        }
    }

@app.get("/points", response_model=GeoJSONFeatureCollection)
async def get_points():
    """Return all points as a GeoJSON FeatureCollection."""
    try:
        feature_collection = {
            "type": "FeatureCollection",
            "features": [to_geojson_feature(point) for point in POINTS]
        }
        return feature_collection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/points/filter", response_model=GeoJSONFeatureCollection)
async def filter_points(filters: FilterCriteria):
    """Filter points based on criteria provided in the JSON body."""
    try:
        filtered_points = POINTS

        # Apply min_value filter if provided
        if filters.min_value is not None:
            filtered_points = [p for p in filtered_points if p["value"] >= filters.min_value]

        # Apply name_contains filter if provided
        if filters.name_contains:
            name_contains = filters.name_contains.lower()
            filtered_points = [p for p in filtered_points if name_contains in p["name"].lower()]

        # Convert to GeoJSON
        feature_collection = {
            "type": "FeatureCollection",
            "features": [to_geojson_feature(point) for point in filtered_points]
        }
        return feature_collection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)