import streamlit as st
from video_processor import process_stream

st.title("Real-Time Video Analytics Dashboard")
source_type = st.radio(
    "Select video source:",
    ["Webcam", "Uploaded file", "Stream URL"],
)

if source_type == "Webcam":
    from streamlit_webrtc import webrtc_streamer

    webrtc_streamer(
        key="video",
        video_frame_callback=process_stream,
        media_stream_constraints={"video": True, "audio": False},
    )
elif source_type == "Uploaded file":
    uploaded_file = st.file_uploader("Upload a video or image", type=["mp4", "avi", "mov", "mkv", "jpg", "jpeg", "png"])
    if uploaded_file is not None:
        import cv2
        import numpy as np
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        # Try image decode first
        image = cv2.imdecode(file_bytes, 1)
        if image is not None:
            # It's an image
            annotated = process_stream(uploaded_file)
            st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB", caption="Processed Image")
        else:
            # Try video decode
            import tempfile
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                tmpfile.write(uploaded_file.read())
                tmpfile_path = tmpfile.name
            cap = cv2.VideoCapture(tmpfile_path)
            stframe = st.empty()
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                annotated = process_stream(frame)
                stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
            cap.release()
elif source_type == "Stream URL":
    url = st.text_input("RTSP/HTTP Stream URL:")
    if url:
        import cv2
        cap = cv2.VideoCapture(url)
        stframe = st.empty()
        if not cap.isOpened():
            st.error("Failed to open stream. Please check the URL.")
        else:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                annotated = process_stream(frame)
                stframe.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), channels="RGB")
            cap.release()
