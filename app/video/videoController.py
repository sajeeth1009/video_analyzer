from flask import Blueprint, request, Response
import json
import logging

# Creating an object
logger = logging.getLogger('gunicorn.error')

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

from app.video.video import *
from app.util.errorHandler import *
from app.video.yoloRecommendations import yolo_recommendations

video_api = Blueprint('video_api', __name__)


@video_api.route('/frames/<videoId>/<samplingRate>', methods=['GET'])
def store_frames(videoId, samplingRate):
    return generateFrames(videoId, samplingRate)


@video_api.route('/tracker')
def track_videos():
    track_object()
    return "success"


@video_api.route('/tracking', methods=['POST'])
def video_tracking():
    logger.info("Incoming /tracking Request: " + str(request.json))
    try:
        video_request = request.json
        video_file = fetch_video(video_request['filename'])
        trackers = generate_trackers(video_request, video_file)
        logger.info("Response : " + json.dumps(trackers))
        return Response(json.dumps(trackers), mimetype='application/json')
    except ValueError as err:
        logger.error("Error Response : " + str(err))
        return ErrorHandler(err.args[0], err.args[1], err.args[2]).report_error()
    except Exception as e:
        logger.error("Error Response : " + str(e))
        return ErrorHandler('E-5000', 'General Error', e.args[0].args[0]).report_error()


@video_api.route('/recommend', methods=['POST'])
def generate_recommendations():
    logger.info
    logger.info("Incoming /recommend Request: " + str(request.json))
    try:
        video_request = request.json
        video_file = fetch_video(video_request['filename'])
        trackers = yolo_recommendations(video_file, video_request)
        logger.info("Response : " + json.dumps(trackers))
        return Response(json.dumps(trackers), mimetype='application/json')
    except ValueError as err:
        logger.error("Error Response : " + str(err))
        return ErrorHandler(err.args[0], err.args[1], err.args[2]).report_error()
    except Exception as e:
        logger.error("Error Response : " + str(e))
        return ErrorHandler('E-5000', 'General Error', e.args[0]).report_error()
