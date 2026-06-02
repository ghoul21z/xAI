import os
import cv2
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

images = [
    "4bb01edb-2207-4ffb-baf7-d3cb80740184.jpg",
    "5436caa6-5655-406d-b88e-d43e7e405caa.jpg",
    "a71a2b00-1186-4548-b593-a366c3576f3c.jpg"
]

out = []
out.append("Advanced Facial Features & Object Detection Report:")

for filename in images:
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        out.append(f"\nFile {filename} does not exist.")
        continue
    
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        out.append(f"\nCould not read {filename}")
        continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30,30))
    
    out.append(f"\n==========================================")
    out.append(f"IMAGE: {filename} ({img.shape[1]}x{img.shape[0]} px)")
    out.append(f"Total Faces Detected: {len(faces)}")
    
    for i, (x, y, w, h) in enumerate(faces):
        out.append(f"\n--- Face {i+1} ---")
        out.append(f"  Position: x={x}, y={y}, w={w}, h={h}")
        
        # Crop face ROI
        face_gray = gray[y:y+h, x:x+w]
        face_color = img[y:y+h, x:x+w]
        
        # 1. Sharpness/Clarity assessment
        sharpness_var = cv2.Laplacian(face_gray, cv2.CV_64F).var()
        if sharpness_var > 300:
            clarity = "High Clarity"
        elif sharpness_var > 120:
            clarity = "Good Clarity"
        elif sharpness_var > 45:
            clarity = "Moderate Clarity"
        else:
            clarity = "Blurry/Low Clarity"
        out.append(f"  Clarity level: {clarity} (Laplacian var: {sharpness_var:.1f})")
        
        # 2. Angle / Pose estimation
        eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=3)
        out.append(f"  Eyes detected inside face box: {len(eyes)}")
        
        if len(eyes) >= 2:
            pose = "Frontal Pose (Thang)"
        elif len(eyes) == 1:
            eye_x = eyes[0][0] + eyes[0][2] / 2
            if eye_x < w / 2:
                pose = "Turned Right (Nghieng phai)"
            else:
                pose = "Turned Left (Nghieng trai)"
        else:
            pose = "Frontal or slight angle (No eyes detected)"
        out.append(f"  Estimated pose: {pose}")
        
        # 3. Glasses / Mask Detection
        # Check glasses
        eye_region = face_gray[0:int(h*0.45), :]
        edges = cv2.Canny(eye_region, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        has_glasses = "Likely Wearing Glasses (Co kinh)" if edge_density > 0.08 else "Not Wearing Glasses (Khong kinh)"
        out.append(f"  Glasses detection: {has_glasses} (Edge density: {edge_density:.3f})")
        
        # Check mask
        mouth_region = face_gray[int(h*0.6):, :]
        mouth_color = face_color[int(h*0.6):, :]
        mean_bgr = cv2.mean(mouth_color)[:3]
        mouth_var = np.var(mouth_region)
        has_mask = "Mask Detected (Co khau trang)" if mouth_var < 80 else "No Mask Detected (Khong khau trang)"
        out.append(f"  Mask detection: {has_mask} (Luminance variance: {mouth_var:.1f}, mean BGR: {[round(c, 1) for c in mean_bgr]})")

# Print clean report to stdout (ASCII-only) and save to UTF-8 file
report_text = "\n".join(out)
print(report_text)

with open(os.path.join(ROOT_DIR, "scratch", "describe_faces_report.txt"), "w", encoding="utf-8") as f:
    f.write(report_text)
print("\nSaved report to scratch/describe_faces_report.txt successfully.")
