import os

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)
print("Directories created.")

# List files and folders
print("Current directory contents:")
for item in os.listdir("."):
    print(item)

# Find .txt files
print("Text files:")
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)