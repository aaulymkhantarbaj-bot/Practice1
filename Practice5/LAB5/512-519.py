#12
import re

text = input()

# \d{2,} matches sequences of 2 or more consecutive digits
numbers = re.findall(r'\d{2,}', text)

print(" ".join(numbers))

#13
import re

text = input()

words = re.findall(r'\w+', text)

print(len(words))

#14
import re

text = input()

# Compile a pattern that matches only digits from start to end
pattern = re.compile(r'^\d+$')

if pattern.fullmatch(text):
    print("Match")
else:
    print("No match")

#15
import re

text = input()

# Function to double each digit
def double_digit(match):
    return match.group() * 2

# Replace every digit using the function
result = re.sub(r'\d', double_digit, text)

print(result)

#16
import re

text = input()

# Use parentheses to capture name and age
match = re.search(r'Name: (.*), Age: (.*)', text)

if match:
    name, age = match.groups()
    print(f"{name} {age}")

#17
import re

text = input()

# \b ensures word boundaries
dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', text)

print(len(dates))

#18
import re

text = input()
pattern = input()

# Escape any regex metacharacters in the pattern
literal_pattern = re.escape(pattern)

matches = re.findall(literal_pattern, text)

print(len(matches))

#19
import re

text = input()

# Compile a pattern that matches words (\w+ with word boundaries)
pattern = re.compile(r'\b\w+\b')

words = pattern.findall(text)

print(len(words))