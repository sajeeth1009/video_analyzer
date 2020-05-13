import numpy as np
import time
import cv2
import os
from app.config import config


def get_frame_at_millisecond(vidcap, millsecond):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, millsecond)
    return vidcap.read()


def yolo_recommendations(video_file, video_request):
    labelsPath = os.path.sep.join([config.get('yolo'), "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")

    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                               dtype="uint8")
    weightsPath = os.path.sep.join([config.get('yolo'), "yolov3.weights"])
    configPath = os.path.sep.join([config.get('yolo'), "yolov3.cfg"])
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    result = {}
    try:
        if video_request['videoX'] & video_request['videoY']:
            dim = (int(video_request['videoX']), int(video_request['videoY']))
    except Exception as e:
        dim = None
    vs = video_file
    fps = vs.get(cv2.CAP_PROP_FPS)
    writer = None
    (W, H) = (None, None)
    timestamps = [vs.get(cv2.CAP_PROP_POS_MSEC)]
    try:
        prop = cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        print("[INFO] {} total frames in video".format(total))
    except Exception as e:
        print("[INFO] could not determine # of frames in video")
        print("[INFO] no approx. completion time can be provided")
        total = -1
        raise ValueError('E-2100', 'Failed to find number of frames' + e.args[0])
    calc_timestamps = [0.0]
    while True:
        (grabbed, frame) = get_frame_at_millisecond(vs, calc_timestamps[-1])
        if not grabbed:
            break
        if dim:
            frame = cv2.resize(frame, dim)
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        timestamps.append(vs.get(cv2.CAP_PROP_POS_MSEC))
        calc_timestamps.append(calc_timestamps[-1] + config.get("recommendframerate"))
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()
        boxes = []
        confidences = []
        classIDs = []
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if confidence > config.get('confidence'):
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, config.get('confidence'),
                                config.get('threshold'))
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                           confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        if writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(os.getenv("MULTER_DEST", 'app/assets/')+'out.mp4', fourcc, 30,
                                     (frame.shape[1], frame.shape[0]), True)
            if total > 0:
                elap = (end - start)
                print("[INFO] single frame took {:.4f} seconds".format(elap))
                print("[INFO] estimated total time to finish: {:.4f}".format(
                    elap * total))
        writer.write(frame)
        result[round(calc_timestamps[-1])] = {"bounding boxes": [[x[0]/W, x[1]/H, x[2]/W, x[3]/H] for x in boxes], "confidences": confidences, "classes": [LABELS.__getitem__(x) for x in classIDs]}
    print("[INFO] cleaning up...")
    writer.release()
    vs.release()
    return result



