import os
import hashlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(ROOT_DIR, "uploads")

files = [
    "a71a2b00-1186-4548-b593-a366c3576f3c.jpg",
    "4e2840cf-1e75-4568-b857-f41ceb6580a3.jpg",
    "8b3f111f-7432-4af2-8072-7326dad718ac.jpg",
    "8d4759fb-7df5-4f04-9376-e033df54f6f5.jpg",
    "9929f53f-cb13-4fd5-9479-e8325926a8d9.jpg"
]

print("Small File Hashes:")
for f in files:
    path = os.path.join(UPLOAD_DIR, f)
    with open(path, "rb") as fh:
        h = hashlib.md5(fh.read()).hexdigest()
        print(f"{f}: {h}")
