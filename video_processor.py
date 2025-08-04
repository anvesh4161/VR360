import cv2
import numpy as np
from detectors.yolov8_object import detect_objects
from detectors.face_detector import detect_faces
from detectors.gender_age import predict_gender_age
from detectors.emotion import predict_emotion
from detectors.body_attr import predict_height_weight
from utils.draw import draw_results

def process_stream(input_frame):

    # If input is a frame (NumPy array)
    if isinstance(input_frame, np.ndarray):
        frame = input_frame
    # If using Streamlit WebRTC
    elif hasattr(input_frame, "to_ndarray"):
        frame = input_frame.to_ndarray(format="bgr24")
    # If uploaded file (file-like object)
    elif hasattr(input_frame, "read"):
        file_bytes = np.asarray(bytearray(input_frame.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)
    # If input is a file path (string)
    elif isinstance(input_frame, str):
        frame = cv2.imread(input_frame)
    else:
        raise ValueError("Unsupported input type for process_stream")

    results = detect_objects(frame)
    people = [det for det in results if det["label"] == "person"]

    for person in people:
        x1, y1, x2, y2 = person["bbox"]
        person_crop = frame[y1:y2, x1:x2]
        face_bbox = detect_faces(person_crop)
        if face_bbox:
            fx1, fy1, fx2, fy2 = face_bbox[0]
            face_img = person_crop[fy1:fy2, fx1:fx2]
            gender, age = predict_gender_age(face_img)
            emotion = predict_emotion(face_img)
        else:
            gender, age, emotion = None, None, None
        height, weight = predict_height_weight(person_crop)
        person.update({
            "gender": gender,
            "age": age,
            "emotion": emotion,
            "height": height,
            "weight": weight,
        })

    annotated = draw_results(frame, results)
    return annotated
