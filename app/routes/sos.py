from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter

from app.models.sighting import GeoJsonPoint, Sighting, SosRequest

router = APIRouter()
sightings: list[Sighting] = []  # temporary in-memory store, replaced by Mongo later


@router.post("/sos", status_code=202)
async def create_sos(req: SosRequest) -> dict:
    sighting = Sighting(
        location=GeoJsonPoint(coordinates=[req.longitude, req.latitude]),  # lng FIRST
        animal=req.animal,
        source="human",
        confidence="unverified",
        timestamp=datetime.now(timezone.utc),
    )
    sightings.append(sighting)
    return {"status": "accepted", "id": str(uuid4())}  # placeholder, Mongo _id replaces it