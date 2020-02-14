import sys

import cv2
import requests
import subprocess

from source.app.config import config
from requests.exceptions import ConnectionError


def fetch_video_file(filename):
    return requests.get(config.get('backendUrl')+'project/files/'+filename)


def fetch_video(filename):
    try:
        video = cv2.VideoCapture("assets/" + filename + ".mp4")
        if not video.isOpened():
            file_content = fetch_video_file(filename)
            file = open("assets/" + filename + ".mp4", "wb")
            file.write(file_content.content)
            file.close()
            video = cv2.VideoCapture("assets/" + filename + ".mp4")
        return video
    except FileNotFoundError as e:
        print(e)
        raise ValueError('E-1000', 'Video File was not found', e.args[0].args[0])
    except ConnectionError as e:
        print(e)
        raise ValueError('E-1100', 'Video File was not be obtained from server', e.args[0].args[0])
    except Exception as e:
        print(e)
        raise ValueError('E-5000', 'General Error', e.args[0].args[0])


def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def generateFrames(videoName, samplingRate):
    # length = get_length('assets/'+videoName+'/'+videoName+'.mp4')
    vidcap = cv2.VideoCapture('assets/' + videoName + '/' + videoName + '.mp4')
    vidcap.set(cv2.CAP_PROP_POS_MSEC, 0)  # just cue to 20 sec. position
    success, image = vidcap.read()
    count = 0
    success = True
    while success:
        cv2.imwrite("assets/" + videoName + "/frame%d.jpg" % count, image)  # save frame as JPEG file
        count += 1
        vidcap.set(cv2.CAP_PROP_POS_MSEC, count * int(samplingRate))
        success, image = vidcap.read()
        print('Read a new frame: ', success)


def get_frame_at_millisecond(vidcap, millsecond):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, millsecond)  # just cue to 20 sec. position
    success, image = vidcap.read()
    if success:
        return image  # save frame as JPEG file
    return None


def generate_trackers(video_request, vidcap):
    try:
        trackers = {}
        tracker_type = config.get('tracker')
        tracker = set_tracking_algo(tracker_type)
        ok, frame = vidcap.read()
        dim = (int(video_request['videoX']), int(video_request['videoY']))
        tracker_dimensions = video_request['trackerDimensions']
        resized_frame = cv2.resize(frame, dim)
        bbox = (tracker_dimensions['x'], tracker_dimensions['y'], tracker_dimensions['width'],
                tracker_dimensions['height'])
        ok = tracker.init(resized_frame, bbox)
        if not ok:
            raise ValueError('E-1300', 'Failed to read video', '')
        for millisecond in video_request['requiredTimes']:
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


def track_obj():
    tracker_type = config.get(config.get('tracker'))
    tracker = set_tracking_algo(tracker_type)



def track_object():
    # Set up tracker.
    # Instead of MIL, you can also use
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
    if int(major_ver) < 3 & int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        tracker = set_tracking_algo(tracker_type)
    # Read video
    video = cv2.VideoCapture("assets/bd64f7cabc54345946ad14c2a01e6e29.mp4")
    # Exit if video not opened.
    if not video.isOpened():
        print
        "Could not open video"
        sys.exit()
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print
        'Cannot read video file'
        sys.exit()
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        # Start timer
        timer = cv2.getTickCount()
        # Update tracker
        ok, bbox = tracker.update(frame)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
        # Display result
        cv2.imshow("Tracking", frame)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break


def set_tracking_algo(tracker_type):
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
