# Elastic5GC Probe
This repo is part of Elastic5GC project. You can see info about this project [here!](#)
This is a probe to collect cpu usage of AMF services available in a specific host and send it to resource monitor.

# Pre reqs
* Docker Engine - [How to install](https://docs.docker.com/engine/install/)
* Elastic5GC Monitor - [docs](#) @TODO
* Python 3.5 or superior

# Env Vars
|Variable|Type|Description|
|-|-|-|
|DOCKER_REMOTELY| 0 or 1 |0 - Uses docker socket, 1 - Uses API. Default: 0|
|DOCKER_HOST| string | Host of docker API. Required if DOCKER_REMOTELY equals to 1. Example: tcp://127.0.0.1:2375|
|MONITOR_HOST| string | Host of Elastic5GC Monitor. Required. Example: 192.168.1.1|
|MONITOR_PORT| int |Port of Elastic5GC Monitor. Required. Example: 5000|
|MONITOR_INTERVAL| int | Interval in seconds to collect data of each AMF service. Example: 10|


## Running bare metal

**Install docker python sdk**
``sudo pip install docker``

**Running**
``sudo MONITOR_HOST=localhost MONITOR_PORT=8080 MONITOR_INTERVAL=10 python3.6 src/probe.py``

### Running on docker
To run in a container or remotely you must enable Docker API to accept external requests. You can see how to enable it [here!](https://docs.docker.com/engine/reference/commandline/dockerd/)

**Create environment file**
``cd docker && cp environment.sample enviroment``
>Change configs to match to your setup.

**Running**
``sudo docker-compose up``
