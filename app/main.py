from fastapi import FastAPI
from soco import SoCo, discover
from soco.data_structures import DidlFavorite
from soco.exceptions import SoCoUPnPException
from soco.groups import ZoneGroup
from soco.music_library import MusicLibrary

from app.datastructures import Base_States, Play_Modes, Repeat_States
from app.sonosActions import (
    action_group_mute,
    action_group_volume,
    action_mute,
    action_next,
    action_pause,
    action_play,
    action_play_mode,
    action_previous,
    action_repeat,
    action_shuffle,
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
    zone_info["group"] = get_group_info(zone.group)  # type: ignore
    zone_info["soundbar"] = zone.is_soundbar
    zone_info["dialog_mode"] = zone.dialog_mode
    zone_info["dialog_level"] = zone.dialog_level
    zone_info["night_mode"] = zone.night_mode
    zone_info["equalizer"] = {}
    zone_info["equalizer"]["balance"] = zone.balance
    zone_info["equalizer"]["bass"] = zone.bass
    zone_info["equalizer"]["trebble"] = zone.treble
    zone_info["equalizer"]["loudness"] = zone.loudness
    return zone_info


def get_all_zone_info():
    data = []
    zone: SoCo
    for zone in ZONES.values():
        data.append(get_zone_info(zone))
    return data


def get_zone_master(zone: SoCo) -> SoCo:
    return zone.group.coordinator  # type: ignore


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
        grp = zone.group  # type: ignore
        # print(grp)
        grouplist[grp.uid] = grp
    res = []
    grp: ZoneGroup
    for grp in grouplist.values():
        res.append(get_group_info(grp))
    return res


@app.get("/favorites")
async def favorites():
    zone: SoCo
    for zone in ZONES.values():
        ml = MusicLibrary(soco=zone)
        return ml.get_sonos_favorites()
    return {"error": "unknown zone"}


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
    zone = get_zone_master(zone)
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
    zone = get_zone_master(zone)
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
    zone = get_zone_master(zone)
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
    zone = get_zone_master(zone)
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


@app.get("/{zone_name}/mute/{state}")
async def mute(zone_name, state: Base_States):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    # if state not in BASE_STATES:
    #     return {"error": "unknown state"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_mute(zone, state)
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/groupMute/{state}")
async def groupmute(zone_name, state: Base_States):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    # if state not in BASE_STATES:
    #     return {"error": "unknown state"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        action_group_mute(zone.group, state)  # type: ignore
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}


@app.get("/{zone_name}/favorite/{favorite_name}")
async def favorite(zone_name, favorite_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    zone = get_zone_master(zone)
    ml = MusicLibrary(soco=zone)
    favs = ml.get_sonos_favorites()
    fav: DidlFavorite
    for fav in favs:
        if fav.title == favorite_name:
            uri = fav.get_uri()
            dic = fav.__dict__
            supported_station_types = ["TuneIn Station", "Deezer Station"]
            if dic["description"] in supported_station_types:
                meta = dic["resource_meta_data"]
                # meta = get_tunein_metadata(favorite)
                try:
                    zone.play_uri(uri=uri, meta=meta)
                except SoCoUPnPException:
                    return {"error": "UPnP"}
                return zone.get_current_media_info()
            zone.stop()
            zone.clear_queue()
            zone.add_to_queue(fav.reference)
            zone.play_from_queue(0)
            return zone.get_current_track_info()
    return {"error": "Favorite " + favorite_name + " not found"}


@app.get("/{zone_name}/queue")
async def queue(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    return zone.get_queue()


@app.get("/{zone_name}/play_uri/{uri}")
async def play_uri(zone_name, uri):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    zone.play_uri(uri=uri)
    return zone.get_current_track_info()


@app.get("/{zone_name}/shuffle/{parameter}")
async def shuffle(zone_name, parameter: Base_States):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_shuffle(zone, parameter)
    except SoCoUPnPException:
        return {"error": "action not available"}
    return {"shuffle": zone.shuffle}


@app.get("/{zone_name}/repeat/{parameter}")
async def repeat(zone_name, parameter: Repeat_States):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_repeat(zone, parameter)
    except SoCoUPnPException:
        return {"error": "action not available"}


@app.get("/{zone_name}/play_mode/{parameter}")
async def play_mode(zone_name, parameter: Play_Modes):
    if zone_name not in ZONES:
        return {"error": "unknown zone"}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        return action_play_mode(zone, parameter)
    except SoCoUPnPException:
        return {"error": "action not available"}


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


@app.get("/{zone_name}/leave")
async def leave_zone(zone_name):
    if zone_name not in ZONES:
        return {"error": "unknown zone name: " + zone_name}
    zone: SoCo
    zone = ZONES[zone_name]
    try:
        zone.unjoin()
        return get_group_info(zone.group)  # type: ignore
    except SoCoUPnPException:
        return {"error": "command not available"}
