import os
import cv2
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
eye_cascade_path = cv2.data.haarcascades + 'haarcascade_eye.xml'

print("Using cascade:", cascade_path)
face_cascade = cv2.CascadeClassifier(cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

if face_cascade.empty():
    print("Error: Could not load frontal face cascade classifier.")
else:
    print("Cascade classifier loaded successfully.")

files = [
    "4bb01edb-2207-4ffb-baf7-d3cb80740184.jpg",
    "5436caa6-5655-406d-b88e-d43e7e405caa.jpg",
    "79633383-7ebe-43f3-b008-647130326a34.jpg",
    "ccee74f0-a35c-4ed8-8fc5-4eac162d94fd.jpg"
]

for filename in files:
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        print(f"File {filename} does not exist.")
        continue
        
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Could not read {filename}")
        continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    
    print(f"\nImage: {filename}")
    print(f"  Faces detected: {len(faces)}")
    for i, (x, y, w, h) in enumerate(faces):
        # Calculate sharpness of the face box
        face_roi = gray[y:y+h, x:x+w]
        sharpness = cv2.Laplacian(face_roi, cv2.CV_64F).var()
        
        # Detect eyes in face ROI
        eyes = eye_cascade.detectMultiScale(face_roi)
        
        print(f"  Face {i+1}:")
        print(f"    Position: x={x}, y={y}, w={w}, h={h}")
        print(f"    Sharpness variance: {sharpness:.1f}")
        print(f"    Eyes detected: {len(eyes)}")
        
        # We can guess pose: frontal if eyes are centered and balanced,
        # or we can look at the relative position. But let's check further.
