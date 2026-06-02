import os
import cv2
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

# Path to images
img1_path = os.path.join(UPLOAD_DIR, "4bb01edb-2207-4ffb-baf7-d3cb80740184.jpg")
img2_path = os.path.join(UPLOAD_DIR, "5436caa6-5655-406d-b88e-d43e7e405caa.jpg")
img3_path = os.path.join(UPLOAD_DIR, "a71a2b00-1186-4548-b593-a366c3576f3c.jpg")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def crop_main_face(img_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(30,30))
    if len(faces) == 0:
        return None
    # Pick the largest face detected
    faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
    x, y, w, h = faces[0]
    return img[y:y+h, x:x+w]

face1 = crop_main_face(img1_path)
face2 = crop_main_face(img2_path)
face3 = crop_main_face(img3_path)

print("Comparing Face Crops:")

def compare_two(f1, f2, label):
    if f1 is None or f2 is None:
        print(f"Comparison {label}: Could not crop one or both faces.")
        return
        
    # Resize to 128x128 for normalized comparison
    f1_gray = cv2.cvtColor(cv2.resize(f1, (128, 128)), cv2.COLOR_BGR2GRAY)
    f2_gray = cv2.cvtColor(cv2.resize(f2, (128, 128)), cv2.COLOR_BGR2GRAY)
    
    # 1. Compute structural similarity or correlation
    res = cv2.matchTemplate(f1_gray, f2_gray, cv2.TM_CCOEFF_NORMED)[0][0]
    
    # 2. Histogram correlation
    h1 = cv2.calcHist([f1], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256])
    h2 = cv2.calcHist([f2], [0,1,2], None, [8,8,8], [0,256, 0,256, 0,256])
    cv2.normalize(h1, h1)
    cv2.normalize(h2, h2)
    hist_corr = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)*100
    
    confidence = (res * 0.5 + (hist_corr/100) * 0.5) * 100
    print(f"Comparison {label}:")
    print(f"  Normalized Correlation: {res*100:.1f}%")
    print(f"  Histogram Correlation: {hist_corr:.1f}%")
    print(f"  Aggregated Face Similarity Confidence: {max(0.0, confidence):.1f}%")

compare_two(face1, face2, "Main Face 1 (Image 1) vs Main Face 2 (Image 2)")
compare_two(face2, face3, "Main Face 2 (Image 2) vs Main Face 3 (Image 3)")
compare_two(face1, face3, "Main Face 1 (Image 1) vs Main Face 3 (Image 3)")
