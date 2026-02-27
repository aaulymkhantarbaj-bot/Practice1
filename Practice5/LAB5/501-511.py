#1
import re

s = input()

if re.match(r"Hello", s):
    print("Yes")
else:
    print("No")

#2
import re

s = input()
sub = input()

if re.search(sub, s):
    print("Yes")
else:
    print("No")

#3
import re

s = input().strip()
pattern = input().strip()

matches = re.findall(pattern, s)
print(len(matches))

#4
import re

text = input()

digits = re.findall(r'\d', text)

print(" ".join(digits))


#5
import re

text = input().strip()

pattern = r'^[A-Za-z].*\d$'

if re.match(pattern, text):
    print("Yes")
else:
    print("No")

#6
import re

text = input()

pattern = r'\S+@\S+\.\S+'

match = re.search(pattern, text)

if match:
    print(match.group())
else:
    print("No email")

#7
import re
str=input()
p=input()
r=input()
x=re.sub(p,r,str)
print(x)

#8
import re

text = input()
pattern = input()

parts = re.split(pattern, text)
print(",".join(parts))

#9
import re

text = input()

# \b ensures whole word, [A-Za-z]{3} means exactly 3 letters
words = re.findall(r'\b[A-Za-z]{3}\b', text)

print(len(words))

#10
import re

text = input()

if re.search(r'cat|dog', text):
    print("Yes")
else:
    print("No")

#11
import re

text = input()

uppercase_letters = re.findall(r'[A-Z]', text)

print(len(uppercase_letters))
