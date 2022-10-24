from soco import SoCo


def action_play(zone: SoCo, parameter: str = "") -> dict:
    zone.play()
    return {"Status": "Ok"}


def action_pause(zone: SoCo, parameter: str = "") -> dict:
    zone.pause()
    return {"Status": "Ok"}


def set_relative_volume(zone: SoCo, dir, volume) -> dict:
    if dir == "-":
        volume = int(volume) * -1
    zone.set_relative_volume(volume)
    return {"Status": "Ok"}


def action_volume(zone: SoCo, parameter) -> dict:
    if parameter is None:
        return {"error": "parameter error"}
    if parameter[0] == "+" or parameter[0] == "-":
        return set_relative_volume(zone, parameter[0], parameter[1:])
    if parameter.isnumeric():
        zone.volume = parameter
        return {"Status": "Ok"}
    return {"error": "parameter error"}


def action_next(zone: SoCo, parameter: str = "") -> dict:
    zone.next()
    return {"Status": "Ok"}


def action_previous(zone: SoCo, parameter: str = "") -> dict:
    zone.previous()
    return {"Status": "Ok"}
