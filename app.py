import streamlit as st
import cv2
from PIL import Image
import numpy as np
import io
import base64

st.set_page_config(page_title="Multi-Mode Camera App", layout="centered")

st.title("📸 Universal Camera Access App")
st.markdown("Supports mobile and desktop — choose camera mode manually.")

# ------------------------ #
#  Mode selection
# ------------------------ #
mode = st.selectbox("Select Camera Mode", ["📱 M1: st.camera_input", "💻 M2: OpenCV Video Feed", "🖼️ M3: Upload Image", "🧪 M4: Web JS Snapshot"], index=0)

# ------------------------ #
#  M1: st.camera_input (Mobile-friendly)
# ------------------------ #
if mode.startswith("📱 M1"):
    st.subheader("Mode M1: st.camera_input()")
    img_file = st.camera_input("Take a picture")

    if img_file is not None:
        st.image(img_file, caption="Captured via camera_input", use_column_width=True)

# ------------------------ #
#  M2: OpenCV Video Feed (Desktop only)
# ------------------------ #
elif mode.startswith("💻 M2"):
    st.subheader("Mode M2: OpenCV Video Capture")
    
    run = st.checkbox('Start Camera')
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Could not access camera. This mode works best on desktop with webcam permissions.")
    
    while run and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Failed to grab frame.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    
    if not run and cap.isOpened():
        cap.release()

# ------------------------ #
#  M3: Upload image manually (Universal fallback)
# ------------------------ #
elif mode.startswith("🖼️ M3"):
    st.subheader("Mode M3: Manual Upload")
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# ------------------------ #
#  M4: HTML5 + JS snapshot via webcam
# ------------------------ #
elif mode.startswith("🧪 M4"):
    st.subheader("Mode M4: JS-based Snapshot")
    
    capture_btn = st.button("📸 Capture Webcam Snapshot (JS)")
    
    if capture_btn:
        st.components.v1.html("""
            <script>
            async function captureAndSend() {
                const video = document.createElement('video');
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');

                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    await video.play();

                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    const dataUrl = canvas.toDataURL('image/png');
                    window.parent.postMessage(dataUrl, '*');
                    stream.getTracks().forEach(track => track.stop());
                } catch (err) {
                    alert("Error accessing webcam: " + err);
                }
            }
            captureAndSend();
            </script>
        """, height=0)

        # Placeholder for the image capture
        st.warning("Captured image will be shown here (JS message listener not yet implemented).")

