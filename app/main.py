from fastapi import FastAPI
from soco import SoCo, discover
from soco.exceptions import SoCoUPnPException
from soco.groups import ZoneGroup

from app.sonosActions import (
    action_group_mute,
    action_group_mute_toggle,
    action_group_unmute,
    action_group_volume,
    action_mute,
    action_mute_toggle,
    action_next,
    action_pause,
    action_play,
    action_previous,
    action_unmute,
    action_volume,
)

app = FastAPI()

ZONES = dict[str, SoCo]
ZONES = {}


def update_zone_info():
    for zone in discover():  # type: ignore
        ZONES[zone.player_name] = zone


update_zone_info()


def get_group_info(zone_group: ZoneGroup) -> dict:
    res = {}
    res["uid"] = zone_group.uid
    res["coordinator"] = zone_group.coordinator.player_name
    res["volume"] = zone_group.volume
    res["mute"] = zone_group.mute
    res["members"] = []
    item: SoCo
    for item in zone_group.members:
        res["members"].append(item.player_name)
    return res


def get_zone_info(zone: SoCo):
    zone_info = {}
    zone_info["player_name"] = zone.player_name
    zone_info["volume"] = zone.volume
    zone_info["mute"] = zone.mute
    zone_info["media"] = zone.get_current_media_info()
    zone_info["track"] = zone.get_current_track_info()
    zone_info["transport"] = zone.get_current_transport_info()
    zone_info["radio"] = zone.get_favorite_radio_stations()
    zone_info["group"] = get_group_info(zone.group)  # type: ignore
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


@app.get("/groups")
async def groups():
    update_zone_info()
    zone: SoCo
    grouplist = {}
    for zone in ZONES.values():
        grp: ZoneGroup
        grp = zone.group  #  type: ignore
        # print(grp)
        grouplist[grp.uid] = grp
    res = []
    grp: ZoneGroup
    for grp in grouplist.values():
        res.append(get_group_info(grp))
    return res


@app.get("/pauseall")
async def pauseall():
    for zone in ZONES:
        action_pause(zone)
    return get_all_zone_info()


@app.get("/playall")
@app.get("/resumeall")
async def resume():
    result = []
    for zone in ZONES:
        result.append(action_play(zone))
    return result


# @app.get("/{zone}", tags=["users"])
@app.get("/{zone_name}")
async def info(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    return get_zone_info(ZONES[zone_name])


@app.get("/{zone_name}/play")
async def play(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_play(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/pause")
async def pause(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_pause(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/next")
async def next(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_next(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/previous")
async def previous(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_previous(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/volume/{parameter}")
async def volume(zone_name, parameter):
    if zone_name not in ZONES:
        return {"error": "unknown zone: " + zone_name}

    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_volume(zone, parameter)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/groupVolume/{parameter}")
async def group_volume(zone_name, parameter):
    if zone_name not in ZONES:
        return {"error": "unknown zone: " + zone_name}

    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_group_volume(zone, parameter)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/mute")
async def mute(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_mute(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/unmute")
async def unmute(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_unmute(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/muteToggle")
async def mutetoggle(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_mute_toggle(zone)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/groupMute")
async def groupmute(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        action_group_mute(zone.group)  # type: ignore
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/groupUnmute")
async def groupunmute(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        action_group_unmute(zone.group)  # type: ignore
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/groupMuteToggle")
async def groupmutetoggle(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        action_group_mute_toggle(zone.group)  # type: ignore
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/join/{zone_master}")
async def join_zone(zone_name, zone_master):
    if zone_name not in ZONES:
        return {"error": "unknown zone name: " + zone_name}
    if zone_master not in ZONES:
        return {"error": "unknown zone master: " + zone_master}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        zone.join(ZONES[zone_master])
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}


# @app.get("/{zone_name}/unJoin/{zone_master}")
@app.get("/{zone_name}/unjoin")
# async def join_zones(zone_name, zone_master):
async def unjoin_zone(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone name: " + zone_name}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        zone.unjoin()
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}
