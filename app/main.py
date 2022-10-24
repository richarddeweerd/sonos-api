from fastapi import FastAPI
from soco import SoCo, discover

from app.sonosActions import (
    action_next,
    action_pause,
    action_play,
    action_previous,
    action_volume,
)

# tags_metadata = [
#     {
#         "name": "users",
#         "description": "Operations with users. The **login** logic is also here.",
#     },
#     {
#         "name": "items",
#         "description": "Manage items. So _fancy_ they have their own docs.",
#         "externalDocs": {
#             "description": "Items external docs",
#             "url": "https://fastapi.tiangolo.com/",
#         },
#     },
# ]
# app = FastAPI(openapi_tags=tags_metadata)
app = FastAPI()


ZONES = {}

actions = {
    "next": action_next,
    "pause": action_pause,
    "play": action_play,
    "previous": action_previous,
    "volume": action_volume,
}


def update_zone_info():
    # zonelist = list(discover())
    for zone in discover():  # type: ignore
        ZONES[zone.player_name] = zone


update_zone_info()


def get_zone_info(zone: SoCo):
    zone_info = {}
    zone_info["player_name"] = zone.player_name
    zone_info["volume"] = zone.volume
    zone_info["media"] = zone.get_current_media_info()
    zone_info["track"] = zone.get_current_track_info()
    zone_info["transport"] = zone.get_current_transport_info()
    zone_info["radio"] = zone.get_favorite_radio_stations()
    return zone_info


def get_all_zone_info():
    data = []
    zone: SoCo
    for zone in ZONES.values():
        data.append(get_zone_info(zone))
    return data


@app.get("/zones")
@app.get("/")
async def root():
    update_zone_info()
    return get_all_zone_info()


@app.get("/pauseall")
async def pauseall():
    for zone in ZONES:
        action_pause(zone)
    return get_all_zone_info()


@app.get("/playall")
@app.get("/resumeall")
async def resume():
    for zone in ZONES:
        action_play(zone)
    return get_all_zone_info()


# @app.get("/{zone}", tags=["users"])
@app.get("/{zone}")
async def info(zone):
    if zone not in ZONES:
        return {"error": "unknown zone"}
    return get_zone_info(ZONES[zone])


@app.get("/{zone}/{action}/{parameter}")
async def play(zone, action, parameter=None):
    if zone not in ZONES:
        return {"error": "unknown zone"}
    if action not in actions:
        return {"error": "unknown action"}
    return actions[action](ZONES["zone"], parameter)
