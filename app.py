import streamlit as st
import cv2
import numpy as np
from datetime import datetime
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="Smart Manual Camera", layout="centered")
st.title("📸 Smart Manual Camera")

# Define available modes
camera_modes = {
    "Auto": {},
    "Landscape Mode": {"exposure": -3, "contrast": 50},
    "Low Light Mode": {"brightness": 150, "gain": 3},
    "Milky Way Mode": {"exposure": -6, "iso": 800},
    "Moon Shot Mode": {"zoom": 4, "contrast": 100},
    "Portrait Mode": {"blur": True},
    "HDR Mode": {},
    "Macro Mode": {},
    "Document Scan Mode": {"thresholding": True},
    "B&W Mode": {"grayscale": True}
}

# Camera mode selection (dropdown for better mobile UX)
selected_mode = st.selectbox("Select Camera Mode", list(camera_modes.keys()))

# Camera feed area
frame_placeholder = st.empty()

# Optional capture button
capture = st.button("📷 Capture")

# Get mode-specific settings
mode_settings = camera_modes[selected_mode]

# Initialize camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Apply settings based on selected mode
if "brightness" in mode_settings:
    camera.set(cv2.CAP_PROP_BRIGHTNESS, mode_settings["brightness"])
if "contrast" in mode_settings:
    camera.set(cv2.CAP_PROP_CONTRAST, mode_settings["contrast"])
if "exposure" in mode_settings:
    camera.set(cv2.CAP_PROP_EXPOSURE, mode_settings["exposure"])
if "gain" in mode_settings:
    camera.set(cv2.CAP_PROP_GAIN, mode_settings["gain"])

# Read frame
ret, frame = camera.read()

if ret:
    # Apply grayscale
    if mode_settings.get("grayscale"):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    # Apply blur
    if mode_settings.get("blur"):
        frame = cv2.GaussianBlur(frame, (21, 21), 0)

    # Apply thresholding
    if mode_settings.get("thresholding"):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    # Display video feed
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame, channels="RGB", use_column_width=True)

    # Save image if capture button is pressed
    if capture:
        img_name = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(img_name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        st.success(f"Image saved as {img_name}")
        st.image(frame, caption="Last Capture", use_column_width=True)

camera.release()
