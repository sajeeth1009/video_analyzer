import os
import logging

from flask import Flask
from app.video.videoController import video_api

logging.basicConfig(format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger('gunicorn.error')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

app.register_blueprint(video_api, url_prefix='/video')


@app.route("/")
def live_ping():
    return "Successfully Initialized"


if __name__ == "__main__":
    logger.info("Initialising Application: Video Service")
    logger.info("Host - " + str(os.getenv("FLASK_HOST", "0.0.0.0")))
    logger.info("Debug - True")
    logger.info("Port - " + str(os.getenv("FLASK_PORT", 5000)))
    app.run(host=os.getenv("FLASK_HOST", "0.0.0.0"), debug=True, port=os.getenv("FLASK_PORT", 5000))
