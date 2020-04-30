import sys

from flask import Flask
from app.video.videoController import video_api

app = Flask(__name__)



app.register_blueprint(video_api, url_prefix='/video')

@app.route("/")
def live_ping():
    return "Successfully Initialized"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)