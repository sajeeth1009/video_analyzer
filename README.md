# Video Analyzer
Micro-service run through flask that performs object tracking operations for a video annotation tool


* [Video Analyzer Tool](https://github.com/sajeeth1009/video_analyzer.git) (this repository)

## Quickstart

### 0. Prerequisites:

* [git](https://git-scm.com/downloads) 
* [Docker](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Additionally if the installation is occurring in a windows system, ensure that git checks out files with unix style endings by running the following:

```bash
$ git config --global core.autocrlf false
```


### 1. Clone the repository

This repository served as a service module for the [Video Annotation Tool](https://github.com/phev8/video-annotation-tool/tree/extended-video-annotation)

```bash
$ git clone https://github.com/sajeeth1009/video_analyzer.git
```

### 2. Edit .env

Change `BACKEND_HOST` entry in the `.env` to the IP of the docker daemon that runs the video annotation tool.
This can be obtained by running the following command on the server where the video annotation tool is running.
```bash
docker run --net=host codenvy/che-ip
```

Ensure that the docker service is running before running the above command. On windows systems you can use the docker quickstart terminal to determine the IP of the docker daemon.

You can open the environment file to update the field `BACKEND_HOST` to the correct IP. Additionally also set up the port of the 
backend tier for the video annotation tool by specifying it in the field `BACKEND_PORT`. By default this remains at 3000.
```bash
$ cd video_analyzer
$ nano .env
```

For example:
```dotenv
BACKEND_HOST=172.17.0.1
BACKEND_PORT=3000
```


### 3. Pull containers and bring them up (launch):

```bash
$ cd video_analyzer
$ (sudo) docker-compose up --build
```
This process will take some time and will install the required python packages and will build a running instance of the video analyzer application.

When the process is finished, open your browser and go to  `<docker-host-ip>:5000` to check if the instance is up.


## Troubleshooting

###  Stop and remove containers, networks and volumes

WARNING: This will clear any data you had in your instance. If you wish to save persistent data, try this link 
(TODO: add a link describing how to backup docker volumes)

If you had a previous version running in your system you might want to remove previous containers, networks and volumes. 

```bash
$ docker-compose down
```
Lastly, the entire system can be deleted for re-creation using the command
```bash
$ docker system prune --all
```

---

NOTE: The containers will attempt to use port 5000 for the flask application. Depending on your system you might want to change these values in `docker-compose.yaml`.

