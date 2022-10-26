from soco import SoCo
from soco.groups import ZoneGroup

from app.datastructures import Base_States, Play_Modes, Repeat_States


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


def action_mute(zone: SoCo, state: Base_States) -> dict:
    if state == Base_States.TOGGLE:
        zone.mute = not zone.mute
    if state == Base_States.OFF:
        zone.mute = False
    if state == Base_States.ON:
        zone.mute = True
    zone_info = {}
    zone_info["mute"] = zone.mute
    return zone_info


def action_group_mute(grp: ZoneGroup, state: Base_States):
    if state == Base_States.TOGGLE:
        grp.mute = not grp.mute
    if state == Base_States.OFF:
        grp.mute = False
    if state == Base_States.ON:
        grp.mute = True
    zone_info = {}
    zone_info["mute"] = grp.mute
    return zone_info


def action_repeat(zone: SoCo, state: Repeat_States):
    if state == Repeat_States.ON:
        zone.repeat = True
    if state == Repeat_States.OFF:
        zone.repeat = False
    if state == Repeat_States.TOGGLE:
        zone.repeat = not zone.repeat
    if state == Repeat_States.ONE:
        zone.repeat = "ONE"
    zone_info = {}
    zone_info["repeat"] = zone.repeat
    return zone_info


def action_shuffle(zone: SoCo, state: Base_States):
    if state == Base_States.ON:
        zone.shuffle = True
    if state == Base_States.OFF:
        zone.shuffle = False
    if state == Base_States.TOGGLE:
        zone.shuffle = not zone.shuffle
    zone_info = {}
    zone_info["shuffle"] = zone.shuffle
    return zone_info


def action_play_mode(zone: SoCo, state: Play_Modes):
    if state == Play_Modes.NORMAL:
        zone.play_mode = "NORMAL"
    if state == Play_Modes.REPEAT_ALL:
        zone.play_mode = "REPEAT_ALL"
    if state == Play_Modes.REPEAT_ONE:
        zone.play_mode = "REPEAT_ONE"
    if state == Play_Modes.SHUFFLE:
        zone.play_mode = "SHUFFLE"
    if state == Play_Modes.SHUFFLE_NOREPEAT:
        zone.play_mode = "SHUFFLE_NOREPEAT"
    if state == Play_Modes.SHUFFLE_REPEAT_ONE:
        zone.play_mode = "SHUFFLE_REPEAT_ONE"
    zone_info = {}
    zone_info["repeat"] = zone.repeat
    zone_info["shuffle"] = zone.shuffle
    return zone_info
