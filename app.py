from streamlit_webrtc import webrtc_streamer
import streamlit as st
import av
import cv2
import numpy as np

st.set_page_config(page_title="Redmi 10 Prime Camera App", layout="wide")

st.title("📸 Redmi 10 Prime - Advanced Camera Streamlit App")

st.markdown("""
Welcome to the **Streamlit Camera App** for **Redmi 10 Prime**!  
Select a camera mode below to simulate various photography styles using software processing.

**Supported Modes**:
- 🌄 Landscape Mode
- 🌌 Milky Way Mode
- 🌕 Moon Shot Mode
- 🌙 Night Mode
- 🌞 Daylight Mode
- 🤳 Portrait Mode
- 🎨 Manual WB (White Balance) Mode
- 🟣 Vintage Filter
- 🖤 Black & White
- 🧊 Cool Tone
- 🔥 Warm Tone
""")

mode = st.selectbox(
    "Select Camera Mode",
    [
        "Default",
        "Landscape",
        "Milky Way",
        "Moon Shot",
        "Night Mode",
        "Daylight",
        "Portrait",
        "Manual White Balance",
        "Vintage",
        "Black & White",
        "Cool Tone",
        "Warm Tone",
    ]
)

# Manual White Balance sliders
if mode == "Manual White Balance":
    red_gain = st.slider("Red Gain", 0.5, 2.0, 1.0, 0.01)
    blue_gain = st.slider("Blue Gain", 0.5, 2.0, 1.0, 0.01)

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        if mode == "Landscape":
            img = cv2.convertScaleAbs(img, alpha=1.2, beta=20)
        elif mode == "Milky Way":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.equalizeHist(img)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif mode == "Moon Shot":
            img = cv2.convertScaleAbs(img, alpha=1.5, beta=30)
        elif mode == "Night Mode":
            img = cv2.GaussianBlur(img, (3, 3), 0)
            img = cv2.convertScaleAbs(img, alpha=1.3, beta=15)
        elif mode == "Daylight":
            img = cv2.convertScaleAbs(img, alpha=1.1, beta=10)
        elif mode == "Portrait":
            img = cv2.GaussianBlur(img, (11, 11), 10)
        elif mode == "Manual White Balance":
            b, g, r = cv2.split(img)
            r = cv2.convertScaleAbs(r, alpha=red_gain)
            b = cv2.convertScaleAbs(b, alpha=blue_gain)
            img = cv2.merge([b, g, r])
        elif mode == "Vintage":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.applyColorMap(img, cv2.COLORMAP_PINK)
        elif mode == "Black & White":
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif mode == "Cool Tone":
            img = cv2.applyColorMap(img, cv2.COLORMAP_OCEAN)
        elif mode == "Warm Tone":
            img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="camera", video_processor_factory=VideoProcessor)
