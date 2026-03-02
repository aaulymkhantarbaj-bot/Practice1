import shutil
import os

# Ensure destination folder exists
os.makedirs("parent", exist_ok=True)

# Move file
if os.path.exists("sample.txt"):
    shutil.move("sample.txt", "parent/sample.txt")
    print("File moved.")
else:
    print("sample.txt not found.")