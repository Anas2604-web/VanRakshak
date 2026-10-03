from datetime import datetime
from typing import Literal, List, Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator, field_validator, ConfigDict

# 1. HELPER FOR MONGO OBJECT ID SERIALIZATION
# Converts MongoDB BSON ObjectId into a clean string for frontend clients
PyObjectId = Annotated[str, BeforeValidator(str)]

# 2. STRICT GEOJSON SUB-MODEL
class GeoJsonPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float]  # [longitude, latitude]

    @field_validator('coordinates')
    @classmethod
    def validate_coordinates(cls, coords: List[float]) -> List[float]:
        if len(coords) != 2:
            raise ValueError("Coordinates array must contain exactly [longitude, latitude].")

        lon, lat = coords
        if not (-180.0 <= lon <= 180.0):
            raise ValueError(f"Longitude {lon} must stay between -180 and 180.")
        if not (-90.0 <= lat <= 90.0):
            raise ValueError(f"Latitude {lat} must stay between -90 and 90.")
        return coords

class Sighting(BaseModel):
    # id can be missing (new sighting) OR a string (once Mongo assigns one)
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    location: GeoJsonPoint
    animal: Literal["tiger", "leopard", "elephant", "bear"]
    source: Literal["human", "camera_trap", "simulated_camera_trap"]
    confidence: Literal["unverified", "likely", "confirmed"] = "unverified"
    timestamp: datetime

    model_config = ConfigDict(
        populate_by_name=True,
    )