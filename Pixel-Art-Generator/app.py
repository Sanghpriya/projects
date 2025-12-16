import streamlit as st
import numpy as np
from PIL import Image
import cv2
import os
import sys

# Ensure same directory imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pixel_art import (
    pixel_art_pipeline,
    apply_palette,
    PALETTES
)

st.set_page_config(layout="wide")
st.title("Pixel Art Generator")

# ------------------ UPLOAD ------------------

uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

# ------------------ SIDEBAR CONTROLS ------------------

st.sidebar.header("Controls")

pixel_size = st.sidebar.slider("Pixel Size", 4, 32, 16)
colors = st.sidebar.slider("Number of Colors", 4, 32, 16)
edge_thick = st.sidebar.slider("Outline Thickness", 1, 3, 1)

style = st.sidebar.selectbox(
    "Style",
    ["Custom", "NES", "GameBoy", "Pico-8"]
)

# ------------------ CACHED PIPELINE ------------------

@st.cache_data(show_spinner=False)
def run_pipeline(img, pixel_size, colors, edge_thick, style):
    use_quant = (style == "Custom")

    result = pixel_art_pipeline(
        img.copy(),
        pixel_size,
        colors,
        edge_thick,
        use_quant=use_quant
    )

    if style != "Custom":
        result = apply_palette(result, PALETTES[style])

    return result

# ------------------ PROCESS ------------------

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    img_np = np.array(img)

    result = run_pipeline(
        img_np,
        pixel_size,
        colors,
        edge_thick,
        style
    )

    col1, col2 = st.columns(2)

    col1.image(img, caption="Original", width=350)
    col2.image(result, caption="Pixel Art", width=350)

    # Download
    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".png", result_bgr)

    st.download_button(
        "⬇Download Pixel Art",
        buffer.tobytes(),
        file_name="pixel_art.png",
        mime="image/png"
    )
