from flask import Blueprint, request, Response
import json

from source.app.video.video import *
from source.app.util.errorHandler import *
from source.app.video.yoloRecommendations import yolo_recommendations

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
    print("Incoming /tracking Request: " + str(request.json))
    try:
        video_request = request.json
        video_file = fetch_video(video_request['filename'])
        trackers = generate_trackers(video_request, video_file)
        print("Response : " + json.dumps(trackers))
        return Response(json.dumps(trackers), mimetype='application/json')
    except ValueError as err:
        return ErrorHandler(err.args[0], err.args[1], err.args[2]).report_error()
    except Exception as e:
        return ErrorHandler('E-5000', 'General Error', e.args[0].args[0]).report_error()


@video_api.route('/recommend', methods=['POST'])
def generate_recommendations():
    print("Incoming /recommend Request: " + str(request.json))
    try:
        video_request = request.json
        video_file = fetch_video(video_request['filename'])
        trackers = yolo_recommendations(video_file, video_request)
        print("Response : " + json.dumps(trackers))
        return Response(json.dumps(trackers), mimetype='application/json')
    except ValueError as err:
        return ErrorHandler(err.args[0], err.args[1], err.args[2]).report_error()
    except Exception as e:
        return ErrorHandler('E-5000', 'General Error', e.args[0]).report_error()
