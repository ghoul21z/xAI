import os
import hashlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

f1 = os.path.join(UPLOAD_DIR, "5436caa6-5655-406d-b88e-d43e7e405caa.jpg")
f2 = os.path.join(UPLOAD_DIR, "79633383-7ebe-43f3-b008-647130326a34.jpg")
f3 = os.path.join(UPLOAD_DIR, "ccee74f0-a35c-4ed8-8fc5-4eac162d94fd.jpg")

def md5(p):
    if not os.path.exists(p):
        return None
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

print("File Hashes:")
print("5436...:", md5(f1))
print("7963...:", md5(f2))
print("ccee...:", md5(f3))
