# VanRakshak (वनरक्षक) - Backend

Human-wildlife conflict reporting and alert system, inspired by real human-tiger/leopard conflict near Bandhavgarh Tiger Reserve, MP.

**Status: 🚧 Work in progress.** `/sos` now persists to MongoDB with a geospatial index. Alerts, confidence scoring and the map are next.

## Why
Villagers near tiger reserves get injured on grazing and forest trips. Tadoba Tiger Reserve runs a hardware-based warning system (thermal cameras + village sirens). VanRakshak aims to be a **software-only** version that any reserve can deploy without special equipment.

## Roadmap
- [x] FastAPI app + health check
- [x] `POST /sos`: validated instant-alert endpoint
- [x] MongoDB (Motor) persistence with 2dsphere geospatial index
- [ ] Nearby-sightings query (radius + time window)
- [ ] Confidence scoring (unverified, likely, confirmed)
- [ ] Redis pub/sub worker: async fan-out to nearby users
- [ ] Standard sighting report endpoint
- [ ] Ranger map (Leaflet) + natural-language query layer (LangGraph)

## API

### `POST /sos`
One-tap alert. The client sends only the animal and GPS position. The server sets `source`, `confidence` and `timestamp`, so a client can never fake a verified report.

```json
{"animal": "tiger", "latitude": 23.52, "longitude": 80.84}
```

Returns `202 Accepted`: `{"status": "accepted", "id": "..."}` where `id` is the MongoDB document id.
Invalid input (animal not in tiger/leopard/elephant/bear, or coordinates out of range) returns `422`.

Each report is stored in the `sightings` collection with a GeoJSON `location` (`[longitude, latitude]`) and a UTC timestamp.

### `GET /health`
Returns `{"status": "ok"}`.

## Design decisions
- **Two models:** `SosRequest` (what the phone sends) vs `Sighting` (what is stored). The server owns trust-related fields.
- **202, not 201:** the endpoint acknowledges receipt; slower work (nearby-user lookup) will run asynchronously via Redis.
- **GeoJSON validation at the boundary:** bad coordinates fail with a clean 422 instead of a database error.
- **`source` field** (`human | camera_trap | simulated_camera_trap`): a future camera and vision model can post to the same endpoint with no redesign.
- **One shared async Mongo client** created at startup (FastAPI lifespan) and closed at shutdown; a `2dsphere` index is created on `sightings.location` for radius queries.

## Known limitations
- Many villagers lack phones or reliable internet. **Rangers and field staff are the realistic primary reporters.** An offline-first queue will help with intermittent signal, not zero signal.
- Report verification is heuristic and **not a solved problem**. A forest officer's action always overrides.
- No villager safety advice is included yet. Generic online tips are written for safari tourists and don't apply to someone on foot. This will be added only once sourced from the local forest range office.

## Run locally
```powershell
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # then fill in MONGODB_URI and DB_NAME
uvicorn app.main:app --reload
```
Needs a MongoDB instance (a free Atlas M0 cluster works). Never commit `.env`.
Docs at `http://127.0.0.1:8000/docs`.

## Stack
FastAPI · Pydantic v2 · MongoDB (Motor) · Redis (planned) · Next.js frontend (separate repo)