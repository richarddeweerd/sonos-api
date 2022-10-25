from soco import SoCo
from soco.groups import ZoneGroup


def action_play(zone: SoCo) -> dict:
    zone.play()
    zone_info = {}
    zone_info["transport"] = zone.get_current_transport_info()
    zone_info["media"] = zone.get_current_media_info()
    zone_info["track"] = zone.get_current_track_info()
    return zone_info


def action_pause(zone: SoCo) -> dict:
    zone.pause()
    zone_info = {}
    zone_info["transport"] = zone.get_current_transport_info()
    return zone_info


def set_relative_volume(zone: SoCo, dir, volume) -> dict:
    if dir == "-":
        volume = int(volume) * -1
    zone.set_relative_volume(volume)
    return {"Volume": zone.volume}


def set_relative_group_volume(grp: ZoneGroup, dir, volume) -> dict:
    if dir == "-":
        volume = int(volume) * -1
    grp.set_relative_volume(volume)
    return {"Volume": grp.volume}


def action_volume(zone: SoCo, parameter) -> dict:
    if parameter is None:
        return {"error": "parameter error"}
    if parameter[0] == "+" or parameter[0] == "-":
        return set_relative_volume(zone, parameter[0], parameter[1:])
    if parameter.isnumeric():
        zone.volume = parameter
        return {"Volume": zone.volume}
    return {"error": "parameter error"}


def action_group_volume(zone: SoCo, parameter) -> dict:
    grp: ZoneGroup
    grp = zone.group  # type: ignore
    if parameter is None:
        return {"error": "parameter error"}
    if parameter[0] == "+" or parameter[0] == "-":
        return set_relative_group_volume(grp, parameter[0], parameter[1:])
    if parameter.isnumeric():
        grp.volume = parameter
        return {"Volume": grp.volume}
    return {"error": "parameter error"}


def action_next(zone: SoCo) -> dict:
    zone.next()
    zone_info = {}
    zone_info["track"] = zone.get_current_track_info()
    return zone_info


def action_previous(zone: SoCo) -> dict:
    zone.previous()
    zone_info = {}
    zone_info["track"] = zone.get_current_track_info()
    return zone_info


def action_mute(zone: SoCo) -> dict:
    zone.mute = True
    zone_info = {}
    zone_info["mute"] = zone.mute
    return zone_info


def action_unmute(zone: SoCo) -> dict:
    zone.mute = False
    zone_info = {}
    zone_info["mute"] = zone.mute
    return zone_info


def action_mute_toggle(zone: SoCo) -> dict:
    zone.mute = not zone.mute

    zone_info = {}
    zone_info["mute"] = zone.mute
    return zone_info


def action_group_mute(grp: ZoneGroup):
    grp.mute = True
    return


def action_group_unmute(grp: ZoneGroup):
    grp.mute = False
    return


def action_group_mute_toggle(grp: ZoneGroup):
    grp.mute = not grp.mute
    return
