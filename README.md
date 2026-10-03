# VanRakshak (वनरक्षक)

Human-wildlife conflict reporting and alert system, inspired by real human-tiger/leopard conflict near Bandhavgarh Tiger Reserve, MP.

**Status: 🚧 Work in progress**

## Planned
- One-tap SOS alerts (tiger / leopard / elephant / bear) with auto-GPS
- Standard sighting reports with a confidence-scored map
- Natural-language ranger queries over geospatial data

## Stack
FastAPI · MongoDB (2dsphere) · Redis pub/sub · Next.js · LangGraph

## Run locally
    pip install -r requirements.txt
    uvicorn app.main:app --reload