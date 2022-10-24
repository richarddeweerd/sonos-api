from fastapi import FastAPI
from soco import SoCo, discover

app = FastAPI()

ZONES = {}

def update_zone_info():    
    zonelist = list(discover())
    for zone in zonelist:
        ZONES[zone.player_name] = zone
    

update_zone_info()

def get_zone_info(zone:SoCo):
    zone_info = {}
    zone_info["player_name"] = zone.player_name
    zone_info["volume"] = zone.volume
    zone_info["media"] = zone.get_current_media_info()
    zone_info["track"] = zone.get_current_track_info()
    zone_info["transport"] = zone.get_current_transport_info()    
    return zone_info

def get_all_zone_info(zones):
    data = []
    for zone in ZONES:
        data.append(get_zone_info(ZONES[zone]))
    return data



@app.get("/")
async def root():
    update_zone_info()
    return get_all_zone_info(ZONES)

@app.get("/zones")
async def zones():
    update_zone_info()
    return get_all_zone_info(ZONES)

@app.get("/{zone}")
async def info(zone):
    if zone not in ZONES:        
        return {"error": "unknown zone"}
    return get_zone_info(ZONES[zone])

@app.get("/{zone}/play")
async def play(zone):
    if zone in ZONES:
        ZONES[zone].play()
        return get_zone_info(ZONES[zone])
    if zone == "ALL":
        for zone in ZONES:
            ZONES[zone].play()
        return get_all_zone_info(ZONES)


@app.get("/{zone}/pause")
async def pause(zone):
    if zone in ZONES:
        ZONES[zone].pause()
        return get_zone_info(ZONES[zone])
    if zone == "ALL":
        for zone in ZONES:
            ZONES[zone].pause()
        return get_all_zone_info(ZONES)

@app.get("/{zone}/volume/{target}")
async def volume(zone, target):
    if zone in ZONES:
        ZONES[zone].volume = target 
        return get_zone_info(ZONES[zone])
    if zone == "ALL":
        for zone in ZONES:
            ZONES[zone].volume = target
        return get_all_zone_info(ZONES)

