import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Root:", root)
for item in os.listdir(root):
    full_path = os.path.join(root, item)
    if os.path.isdir(full_path):
        print(f"Dir: {item}")
    else:
        print(f"File: {item} ({os.path.getsize(full_path)} bytes)")
