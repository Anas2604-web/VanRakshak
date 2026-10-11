from datetime import datetime

async def find_nearby(db, animal: str, lng: float, lat: float,
                      radius_m: int, since: datetime) -> list[dict]:
    query = {
        "animal": animal,
        "timestamp": {"$gte": since},
        "location": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lng, lat]},
                "$maxDistance": radius_m,
            }
        },
    }
    cursor = db["sightings"].find(query)
    return await cursor.to_list(length=100)

