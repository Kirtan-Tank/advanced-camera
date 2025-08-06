import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(layout="wide")
st.title("📷 Smart Camera Web App")

# Define modes and their descriptions
modes = {
    "Normal": "Standard photo with no enhancement.",
    "Low Light Mode": "Brightens dark areas for night photography.",
    "Moon Shot Mode": "Increases contrast and sharpness for moon shots.",
    "Milky Way Mode": "Simulates long exposure with light enhancement.",
    "Landscape Mode": "Boosts saturation and sharpness for scenery.",
    "Portrait Mode": "Applies slight blur to background.",
    "Black & White": "Grayscale photography.",
    "HDR Simulation": "Enhances contrast and vibrancy.",
    "Vintage Filter": "Adds a warm, retro tone.",
    "Cinematic Mode": "Widescreen crop with color grading."
}

selected_mode = st.selectbox("📸 Select Camera Mode", options=list(modes.keys()))
st.markdown(f"ℹ️ **{modes[selected_mode]}**")

FRAME_WIDTH = 800

# OpenCV camera feed
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    st.error("⚠️ Unable to access your camera. Make sure it's allowed in browser settings.")
else:
    ret, frame = camera.read()
    if ret:
        # Apply selected mode
        if selected_mode == "Low Light Mode":
            frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=30)

        elif selected_mode == "Moon Shot Mode":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.equalizeHist(gray)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        elif selected_mode == "Milky Way Mode":
            frame = cv2.GaussianBlur(frame, (7, 7), 1)
            frame = cv2.convertScaleAbs(frame, alpha=1.7, beta=40)

        elif selected_mode == "Landscape Mode":
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv[..., 1] = hsv[..., 1] * 1.3  # Increase saturation
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        elif selected_mode == "Portrait Mode":
            mask = np.zeros_like(frame)
            h, w, _ = frame.shape
            center = (w // 2, h // 2)
            cv2.circle(mask, center, min(center) // 2, (255, 255, 255), -1)
            blurred = cv2.GaussianBlur(frame, (31, 31), 0)
            frame = np.where(mask == np.array([255, 255, 255]), frame, blurred)

        elif selected_mode == "Black & White":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        elif selected_mode == "HDR Simulation":
            hdr = cv2.detailEnhance(frame, sigma_s=12, sigma_r=0.15)
            frame = cv2.addWeighted(frame, 0.6, hdr, 0.4, 0)

        elif selected_mode == "Vintage Filter":
            vintage = np.array([0.93, 0.79, 0.69])
            frame = np.clip(frame * vintage, 0, 255).astype(np.uint8)

        elif selected_mode == "Cinematic Mode":
            h, w, _ = frame.shape
            new_h = int(w * 9 / 21)  # 21:9 aspect
            y1 = (h - new_h) // 2
            y2 = y1 + new_h
            frame = frame[y1:y2, :, :]
            frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

        # Resize and show
        frame = cv2.resize(frame, (FRAME_WIDTH, int(frame.shape[0] * FRAME_WIDTH / frame.shape[1])))
        st.image(frame, channels="BGR", use_column_width=True)
    else:
        st.error("⚠️ Failed to read frame from camera.")

camera.release()
