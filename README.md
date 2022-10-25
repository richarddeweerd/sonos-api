# Sonos-API
## Description
sonos-api is a easy and simple http api gatway to control the Sonos devices in the network.

- [ ] Github repo: https://github.com/richarddeweerd/sonos-api/
- [ ] Docker Hub: https://hub.docker.com/r/rdweerd/sonos-api

The code is based on: 
- [ ] Python
- [ ] [FastApi](https://fastapi.tiangolo.com/)
- [ ] [SoCo](https://github.com/SoCo/SoCo)

For compatibility it mimics the API of [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) by [jishi](https://github.com/jishi)

## Installation
Sonos API is available as a Docker image, install with the following Docker command:
```
docker pull rdweerd/sonos-api
```

After installation the service is running on port 8080

# Usage

Swagger file http://\<sonos-api\>/docs

## Currently supported endpoints:
```
/
/zones
/playall
/pauseall
/resumeall
/{zone_name}
/{zone_name}/{action}/{parameter}
```


# Actions
## /zones
Any call to http://<sonos-api>:8080/ and http://<sonos-api>:8080/zones will rescan the network for new Sonos devices and return all the zone information
## /<zone_name>
Returns the info of a specific zone

# Zone actions
## Currently supported zone actions:

[next](#next)  
[pause](#pause)  
[play](#play)  
[previous](#previous)  
[volume](#volume)  
[groupVolume](#groupvolume)  
[mute](#mute)  
[unmute](#unmute)  
[muteToggle](#mutetoggle)  
[join](#join)  
[unjoin](#unjoin)  

## next
Next item in the queue
## pause
Pauses playout
## play
Starts playout
## previous
Previous item in the queue
## volume
Changes the volume of the zone.
The parameter is absolute or relative. If the volume is prefixed with +/- it will be treated as a relative volume change

Examples:

    /<zone_name>/volume/10      Sets the volume to 10 percent
    /<zone_name>/volume/+10     Increases the volume with 10 percent
    /<zone_name>/volume/-10     Decreases the volume with 10 percent

## groupVolume
Changes the volume of the group where this zone is part of.
The parameter is absolute or relative. If the volume is prefixed with +/- it will be treated as a relative volume change

Examples:

    /<zone_name>/groupVolume/10      Sets the volume to 10 percent
    /<zone_name>/groupVolume/+10     Increases the volume with 10 percent
    /<zone_name>/groupVolume/-10     Decreases the volume with 10 percent

## mute
Mutes the zone
## unmute
Unmutes the zone
## muteToggle
Toggles the mute state of the zone
## groupMute
Mutes the group
## groupUnmute
Unmutes the group
## groupMuteToggle
Toggles the mute state of the group
## join
Joins the zone into the zone_master

    /<zone_name>/join/<zone_master>
## unjoin
Unjoins the zone from the group
