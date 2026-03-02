# Create and write to file

with open("sample.txt", "w") as file:
    file.write("Hello, this is a sample file.\n")
    file.write("Python file handling practice.\n")

# Append new line
with open("sample.txt", "a") as file:
    file.write("New line added.\n")

print("File created and updated.")