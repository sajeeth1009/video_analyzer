import sys
import logging
import cv2
import requests
import os
import subprocess

from app.config import config
from requests.exceptions import ConnectionError

# Creating an object
logger = logging.getLogger('gunicorn.error')

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def fetch_video_file(filename):
    logger.info("Fetching Video File: " + filename)
    url = os.getenv("BACKEND_URL", "http://localhost:3000/") + 'project/files/'+filename
    headers = {'User-Agent': 'curl/7.52.1',
               "accept": '*/*'}
    logger.info("Requesting Backend at :" + url)
    resp = requests.get(url, headers=headers)
    logger.info(resp.status_code)
    return resp


def fetch_video(filename):
    try:
        logger.info("attempting to fetch file from video volume")
        video = cv2.VideoCapture(os.getenv("MULTER_DEST", 'app/assets/') + filename + ".mp4")
        if not video.isOpened():
            file_content = fetch_video_file(filename)
            logger.info("Received File Content : " + str(file_content))
            file = open(os.getenv("MULTER_DEST", 'app/assets/') + filename + ".mp4", "wb")
            file.write(file_content.content)
            file.close()
            video = cv2.VideoCapture(os.getenv("MULTER_DEST", 'app/assets/') + filename + ".mp4")
        return video
    except FileNotFoundError as e:
        logger.error(str(e.args[0].args[0]))
        raise ValueError('E-1000', 'Video File was not found', e.args[0].args[0])
    except ConnectionError as e:
        logger.error(str(e.args[0].args[0]))
        raise ValueError('E-1100', 'Video File was not be obtained from server', e.args[0].args[0])
    except Exception as e:
        logger.error(str(e.args[0].args[0]))
        raise ValueError('E-5000', 'General Error', e.args[0].args[0])


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def get_frame_at_millisecond(vidcap, millsecond):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, millsecond)
    success, image = vidcap.read()
    if success:
        return image
    return None


def generate_trackers(video_request, vidcap):
    try:
        trackers = {}
        tracker_type = config.get('tracker')
        tracker = set_tracking_algorithm(tracker_type)
        frame = get_frame_at_millisecond(vidcap, video_request['initialTrackerTime'])
        dim = (int(video_request['videoX']), int(video_request['videoY']))
        tracker_dimensions = video_request['trackerDimensions']
        resized_frame = cv2.resize(frame, dim)
        bbox = (tracker_dimensions['x'], tracker_dimensions['y'], tracker_dimensions['width'],
                tracker_dimensions['height'])
        ok = tracker.init(resized_frame, bbox)
        if not ok:
            raise ValueError('E-1300', 'Failed to read video', '')
        required_times = video_request['requiredTimes']
        required_times.sort()
        for millisecond in required_times:
            frame = get_frame_at_millisecond(vidcap, millisecond)
            if frame is not None:
                resized_frame = cv2.resize(frame, dim)
                ok, bbox = tracker.update(resized_frame)
                if not ok:
                    trackers['' + str(millisecond)] = {"status": 'E-1400', "message": 'Failed to track object'}
                else:
                    trackers['' + str(millisecond)] = {"status": '200', "message": 'Tracked successfully', "trackerDim": str(bbox)}
            else:
                trackers['' + str(millisecond)] = {"status": 'E-1200', "message": 'Failed to fetch frame'}
        return trackers
    except Exception as e:
        raise ValueError('E-5000', 'General Error', e.args[0])


def set_tracking_algorithm(tracker_type):
    tracker = None
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    return tracker
