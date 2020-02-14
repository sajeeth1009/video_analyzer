from flask import Blueprint, request, Response
import json

from source.app.video.video import *
from source.app.util.errorHandler import *

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
    try:
        video_request = request.json
        video_file = fetch_video(video_request['filename'])
        trackers = generate_trackers(video_request, video_file)
        return Response(json.dumps(trackers), mimetype='application/json')
    except ValueError as err:
        return ErrorHandler(err.args[0], err.args[1], err.args[2]).report_error()
    except Exception as e:
        return ErrorHandler('E-5000', 'General Error', e.args[0].args[0]).report_error()


