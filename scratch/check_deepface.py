import os
import cv2
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

print("Checking if DeepFace is imported successfully:")
try:
    from deepface import DeepFace
    print("DeepFace is available!")
except Exception as e:
    print("DeepFace is not available. Error:", e)
