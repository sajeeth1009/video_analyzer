from flask import Flask

from source.app.video.videoController import video_api

app = Flask(__name__)

app.register_blueprint(video_api, url_prefix='/video')

@app.route("/")
def live_ping():
    return "Successfully Initialized"

if __name__ == "__main__":
    app.run(debug=True)