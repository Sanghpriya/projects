import cv2
import numpy as np


def resize_for_speed(img, max_size=512):
    h, w = img.shape[:2]
    scale = max_size / max(h, w)
    if scale < 1:
        img = cv2.resize(
            img,
            (int(w * scale), int(h * scale)),
            interpolation=cv2.INTER_AREA
        )
    return img

def pixelate(img, pixel_size):
    h, w = img.shape[:2]
    small = cv2.resize(
        img,
        (w // pixel_size, h // pixel_size),
        interpolation=cv2.INTER_LINEAR
    )
    return cv2.resize(
        small,
        (w, h),
        interpolation=cv2.INTER_NEAREST
    )

def quantize(img, k):
    Z = img.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    _, labels, centers = cv2.kmeans(
        Z, k, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS
    )

    centers = np.uint8(centers)
    return centers[labels.flatten()].reshape(img.shape)

def add_edges(img, thickness):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges = cv2.dilate(edges, np.ones((thickness, thickness), np.uint8))
    img[edges > 0] = [0, 0, 0]
    return img

# ------------------ PALETTES ------------------

PALETTES = {
    "NES": np.array([
        [124,124,124], [0,0,252], [0,0,188], [68,40,188],
        [148,0,132], [168,0,32], [168,16,0], [136,20,0]
    ], dtype=np.uint8),

    "GameBoy": np.array([
        [15,56,15], [48,98,48], [139,172,15], [155,188,15]
    ], dtype=np.uint8),

    "Pico-8": np.array([
        [0,0,0], [29,43,83], [126,37,83], [0,135,81],
        [171,82,54], [95,87,79], [194,195,199], [255,241,232]
    ], dtype=np.uint8)
}

# ------------------ PALETTE MAPPING ------------------

def apply_palette(img, palette):
    h, w, _ = img.shape
    img_flat = img.reshape(-1, 3).astype(np.float32)
    palette = palette.astype(np.float32)

    distances = np.linalg.norm(
        img_flat[:, None, :] - palette[None, :, :],
        axis=2
    )

    nearest = np.argmin(distances, axis=1)
    return palette[nearest].reshape(h, w, 3).astype(np.uint8)

# ------------------ pipeline ------------------

def pixel_art_pipeline(img, pixel_size, colors, edge_thick, use_quant=True):
    img = resize_for_speed(img)

    if use_quant:
        img = quantize(img, colors)

    img = pixelate(img, pixel_size)
    img = add_edges(img, edge_thick)

    return img
