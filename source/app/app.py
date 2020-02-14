from flask import Flask

from source.app.video.videoController import video_api

app = Flask(__name__)

app.register_blueprint(video_api, url_prefix='/video')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)