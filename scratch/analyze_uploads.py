import os
import cv2
import numpy as np

# Set directories
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

print("Checking uploads folder:")
files = sorted([f for f in os.listdir(UPLOAD_DIR) if f.endswith(".jpg") or f.endswith(".png")])
for f in files:
    path = os.path.join(UPLOAD_DIR, f)
    size = os.path.getsize(path)
    print(f"File: {f}, Size: {size} bytes")
    
    # Try to read the image
    try:
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            print(f"  Dimensions: {img.shape[1]}x{img.shape[0]} (WxH)")
        else:
            print("  Could not decode image.")
    except Exception as e:
        print(f"  Error reading: {e}")
