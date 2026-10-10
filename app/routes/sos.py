from datetime import datetime, timezone

from fastapi import APIRouter

from app.models.sighting import GeoJsonPoint, Sighting, SosRequest

from app.config.database import get_db

router = APIRouter()


@router.post("/sos", status_code=202)
async def create_sos(req: SosRequest) -> dict:
    sighting = Sighting(
        location=GeoJsonPoint(coordinates=[req.longitude, req.latitude]),
        animal=req.animal,
        source="human",
        confidence="unverified",
        timestamp=datetime.now(timezone.utc),
    )
    doc = sighting.model_dump(by_alias=True, exclude={"id"})
    result = await get_db()["sightings"].insert_one(doc)

    return {"status": "accepted","id": str(result.inserted_id) }