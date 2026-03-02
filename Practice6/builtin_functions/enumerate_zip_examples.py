names = ["Ali", "Aruzhan", "Dana"]
scores = [90, 85, 88]

# enumerate
print("Enumerate example:")
for index, name in enumerate(names):
    print(index, name)

# zip
print("Zip example:")
for name, score in zip(names, scores):
    print(name, score)

# Type checking and conversion
x = "123"
print("Type before:", type(x))

number = int(x)
print("Type after:", type(number))