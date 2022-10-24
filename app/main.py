import re

from fastapi import FastAPI
from soco import SoCo, discover

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


def update_zone_info():
    # zonelist = list(discover())
    for zone in discover():
        ZONES[zone.player_name] = zone


update_zone_info()


def get_zone_info(zone: SoCo):
    zone_info = {}
    zone_info["player_name"] = zone.player_name
    zone_info["volume"] = zone.volume
    zone_info["media"] = zone.get_current_media_info()
    zone_info["track"] = zone.get_current_track_info()
    zone_info["transport"] = zone.get_current_transport_info()
    return zone_info


def get_all_zone_info():
    data = []
    for zone in ZONES:
        data.append(get_zone_info(ZONES[zone]))
    return data


def action_play(zone, parameter):
    ZONES[zone].play()
    return {"Status": "Ok"}


def action_pause(zone, parameter):
    ZONES[zone].pause()
    return {"Status": "Ok"}


def set_relative_volume(zone, dir, volume):
    if dir == "-":
        volume = int(volume) * -1
    ZONES[zone].set_relative_volume(volume)
    return {"Status": "Ok"}


def action_volume(zone, parameter):
    if parameter is None:
        return {"error": "parameter error"}
    if parameter[0] == "+" or parameter[0] == "-":
        return set_relative_volume(zone, parameter[0], parameter[1:])
    if parameter.isnumeric():
        ZONES[zone].volume = parameter
        return {"Status": "Ok"}
    return {"error": "parameter error"}


actions = {"play": action_play, "pause": action_pause, "volume": action_volume}


@app.get("/zones")
@app.get("/")
async def root():
    update_zone_info()
    return get_all_zone_info()


@app.get("/pauseall")
async def pauseall():
    for zone in ZONES:
        ZONES[zone].pause()
    return get_all_zone_info()


@app.get("/playall")
@app.get("/resumeall")
async def resume():
    for zone in ZONES:
        ZONES[zone].play()
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
    return actions[action](zone, parameter)
