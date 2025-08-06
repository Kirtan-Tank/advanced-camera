import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from streamlit_webrtc import WebRtcStreamerState
import av
import cv2
import numpy as np

st.set_page_config(page_title="Manual Camera Modes", layout="centered")

# --- Header
st.title("📸 Manual Camera App")
st.markdown("Toggle between multiple camera modes and filters in real-time!")

# --- Mode Selection
mode = st.selectbox(
    "Choose Camera Mode 🎨",
    [
        "Auto",
        "Low Light",
        "Landscape",
        "Milky Way",
        "Portrait",
        "Moon Shot",
        "Vintage",
        "B&W Classic",
        "HDR",
        "Cartoon",
        "Sketch",
        "Thermal",
        "Invert Colors",
    ],
)

# --- Processing Logic
class VideoProcessor(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        img = frame.to_ndarray(format="bgr24")

        if mode == "Auto":
            return img

        elif mode == "Low Light":
            return cv2.convertScaleAbs(img, alpha=1.3, beta=30)

        elif mode == "Landscape":
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = cv2.add(hsv[:, :, 1], 40)
            hsv[:, :, 2] = cv2.add(hsv[:, :, 2], 30)
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        elif mode == "Milky Way":
            gamma = 1.5
            look_up = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(256)]).astype("uint8")
            return cv2.LUT(img, look_up)

        elif mode == "Portrait":
            return cv2.bilateralFilter(img, 9, 75, 75)

        elif mode == "Moon Shot":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return cv2.merge([gray, gray, gray])

        elif mode == "Vintage":
            sepia = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
            return cv2.transform(img, sepia)

        elif mode == "B&W Classic":
            bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return cv2.merge([bw, bw, bw])

        elif mode == "HDR":
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0)
            cl = clahe.apply(l)
            return cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

        elif mode == "Cartoon":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            return cartoon

        elif mode == "Sketch":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            inv = 255 - gray
            blur = cv2.GaussianBlur(inv, (21, 21), 0)
            sketch = cv2.divide(gray, 255 - blur, scale=256)
            return cv2.merge([sketch, sketch, sketch])

        elif mode == "Thermal":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

        elif mode == "Invert Colors":
            return cv2.bitwise_not(img)

        return img

# --- Camera Feed
ctx = webrtc_streamer(
    key="manual-camera",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# --- Camera Error Message
if ctx.state == WebRtcStreamerState.FAILED:
    st.error("⚠️ Unable to access your camera. Make sure it's allowed in browser settings.")
