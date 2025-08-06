import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Title
st.set_page_config(page_title="Live Camera Filters", layout="wide")
st.markdown("## 📷 Live Camera Filters (Universal)")
st.markdown("Select a mode and allow camera access on mobile/desktop.")

# Function Definitions for Filters
def apply_normal(frame): return frame

def apply_gray(frame): return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_sketch(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)
    return sketch

def apply_sepia(frame):
    sepia = np.array(frame, dtype=np.float64)
    sepia = cv2.transform(sepia, np.matrix([[0.393, 0.769, 0.189],
                                            [0.349, 0.686, 0.168],
                                            [0.272, 0.534, 0.131]]))
    return np.clip(sepia, 0, 255).astype(np.uint8)

def apply_inverted(frame): return cv2.bitwise_not(frame)

def apply_blur(frame): return cv2.GaussianBlur(frame, (15, 15), 0)

def apply_edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def apply_hdr(frame): return cv2.detailEnhance(frame, sigma_s=12, sigma_r=0.15)

def apply_emboss(frame):
    kernel = np.array([[ -2, -1, 0],
                       [ -1,  1, 1],
                       [  0,  1, 2]])
    embossed = cv2.filter2D(frame, -1, kernel) + 128
    return np.clip(embossed, 0, 255).astype(np.uint8)

def apply_thermal(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thermal = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return thermal

def apply_beauty(frame):
    return cv2.bilateralFilter(frame, 9, 75, 75)

# Filter dictionary
filters = {
    "Normal": apply_normal,
    "Gray": apply_gray,
    "Sketch": apply_sketch,
    "Sepia": apply_sepia,
    "Inverted": apply_inverted,
    "Blur": apply_blur,
    "Edge Detection": apply_edge,
    "Cartoon": apply_cartoon,
    "HDR Look": apply_hdr,
    "Emboss": apply_emboss,
    "Thermal": apply_thermal,
    "Beauty (Smooth Skin)": apply_beauty,
}

# Sidebar for mode selection
mode = st.selectbox("Choose Camera Mode:", list(filters.keys()))

# Start camera
frame_placeholder = st.empty()

run = st.toggle("Start Camera", value=False)
cap = None

if run:
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open camera. Please allow camera access.")
        else:
            st.info("Camera started. Use the selector to change modes.")
            while run:
                ret, frame = cap.read()
                if not ret:
                    st.warning("Couldn't read from camera. Try restarting.")
                    break

                # Flip for selfie view
                frame = cv2.flip(frame, 1)

                # Apply selected filter
                filter_fn = filters.get(mode, apply_normal)
                filtered = filter_fn(frame)

                # Convert to RGB for display
                if len(filtered.shape) == 2:
                    filtered = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
                else:
                    filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)

                # Resize feed based on screen
                h, w = filtered.shape[:2]
                scale = 600 / h if h > 600 else 1.5
                resized = cv2.resize(filtered, (int(w * scale), int(h * scale)))

                # Show in Streamlit
                frame_placeholder.image(resized, channels="RGB")

    finally:
        if cap:
            cap.release()
else:
    st.warning("Toggle 'Start Camera' to begin.")
