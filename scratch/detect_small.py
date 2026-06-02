import os
import cv2
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

files = [
    "a71a2b00-1186-4548-b593-a366c3576f3c.jpg",
    "4e2840cf-1e75-4568-b857-f41ceb6580a3.jpg",
    "8b3f111f-7432-4af2-8072-7326dad718ac.jpg",
    "8d4759fb-7df5-4f04-9376-e033df54f6f5.jpg",
    "9929f53f-cb13-4fd5-9479-e8325926a8d9.jpg"
]

for filename in files:
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        continue
        
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=2)
    print(f"File {filename}: {img.shape[1]}x{img.shape[0]} | Faces detected: {len(faces)}")
    for i, (x, y, w, h) in enumerate(faces):
        print(f"  Face {i+1}: position ({x},{y},{w},{h})")
