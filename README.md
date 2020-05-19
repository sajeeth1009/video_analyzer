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

Navigate into the video_analyzer folder and in here first configure the environment variables. The first is the entry `BACKEND_HOST` which tells the video analyzer where the backend for the video annotation tool is running. This is important since the video analyzer needs to connect to the backend to fetch videos to be processed.

Change `BACKEND_HOST` entry in the `.env` to the IP of the docker daemon that runs the [Video Annotation Tool](https://github.com/phev8/video-annotation-tool/tree/extended-video-annotation)

This can be obtained by running the following command on the server where the video annotation tool is running.
```bash
docker run --net=host codenvy/che-ip
```

Ensure that the docker service is running before running the above command. On windows systems you can use the docker quickstart terminal to determine the IP of the docker daemon.

You can open the environment file to update the field `BACKEND_HOST` to the IP address determines above. Additionally also set up the port of the backend tier for the video annotation tool by specifying it in the field `BACKEND_PORT`. By default this remains at 3000. Leave this as is, unless the backend has been forced to run on a different port.
```bash
$ cd video_analyzer
$ nano .env
```

For example:
```dotenv
BACKEND_HOST=172.17.0.1
BACKEND_PORT=3000
```

Similarly, modify the fields `FLASK_HOST` to point to the IP of the docker daemon running the video analyzer software. This can be the same IP as the Video annotation tool if both services are run on the same machine or different IP's if two different docker daemons are used on two different machines. The `FLASK_HOST` represent the IP host of this service while the `FLASK_PORT` represents the port the service runs on. This is set to 5000 by default.

### 3. Pull containers and bring them up (launch):

```bash
$ cd video_analyzer
$ (sudo) docker-compose up --build
```
This process will take some time and will install the required python packages and will build a running instance of the video analyzer application.

When the process is finished, open your browser and go to  `<docker-host-ip>:5000` to check if the instance is up.


## Troubleshooting and Common Errors

### Permission errors

You might encounter errors in connecting to docker daemon either on running the command 
```bash
$ (sudo) docker-compose up --build
```
or on the command 

```bash
docker run --net=host codenvy/che-ip
```

In both cases ensure that docker is installed and docker service is running. If that fails, try running the former command through sudo.


### OpenCV: Transpose not Implemented Error

This occurs since github sometimes doesn't clone the yolo weights correctly. To solve this,
```bash
$ cd video_analyzer/app/video/yolo-coco
$ rm yolov3.weights
$ !wget "https://pjreddie.com/media/files/yolov3.weights"
$ cd ../../../
$ (sudo) docker-compose up --build
```


### Stuck at git clone.

Ensure that sufficient disk space is present. Depending on available bandwidth this clone might take some time since it has to fetch weights for the Yolo model. Also ensure that git lfs installed and initialised in the directory where the clone is to take place.

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

