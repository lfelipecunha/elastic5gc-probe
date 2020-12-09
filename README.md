# Elastic5GC Probe
This repo is part of Elastic5GC project. You can see info about this project [here!](#)
This is a probe to collect cpu usage of AMF services available in a specific host and send it to resource monitor.

# Pre reqs
* Docker Engine - [How to install](https://docs.docker.com/engine/install/)
* Elastic5GC Monitor - [docs](#) @TODO
* Python 3.5 or superior

# Config File

```yml
monitor:
  host: localhost # Host of elastic monitor
  port: 5000 # Port of elastic monitor
  interval: 2 # Interval in seconds between each monitoring
docker:
  remotely: true # Flag to identify if docker is same machine (false) or if it is in another one (true).
  url: tcp://127.0.0.1:2375 # In case of remotely true, specified full url to docker API.
```

## Running bare metal

**Install docker python sdk**

``sudo pip install -r requirements.txt``

**Running**

``sudo src/probe.py --config ../config/probe.yml``

### Running on docker
To run in a container or remotely you must enable Docker API to accept external requests. You can see how to enable it [here!](https://docs.docker.com/engine/reference/commandline/dockerd/)

**Config file**

Change configs located at ``config/probe.yml`` to match to your setup 

**Running**

``sudo docker-compose up``
