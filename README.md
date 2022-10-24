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

## Currently supported zone actions:
```
play
pause
volume/[+/-]<volume>
```
# Actions
## /zones
Any call to http://<sonos-api>:8080/ and http://<sonos-api>:8080/zones will rescan the network for new Sonos devices and return all the zone information
## /<zone_name>
Returns the info of a specific zone

# Zone actions

## play
Starts playout

## pause
Pauses playout

## volume/[+/-]\<volume>
Changes the volume of the zone.
The parameter is absolute or relative. If the volume is prefixed with +/- it will be treated as a relative volume change

Examples:

    /<zone name>/volume/10      Sets the volume to 10 percent
    /<zone name>/volume/+10     Increases the volume with 10 percent
    /<zone name>/volume/-10     Decreases the volume with 10 percent



