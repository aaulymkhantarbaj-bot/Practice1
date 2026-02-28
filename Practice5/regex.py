#1Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.

import re
text = "aaaabbbbbbbbbb"
x = re.search('a*b*', text)
print(x)

#2Write a Python program that matches a string that has an 'a' followed by two to three 'b'

import re
pattern = r'ab{2,3}'
text = input()

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")


#3Write a Python program to find sequences of lowercase letters joined with a underscore.
import re

text = input()
print(bool(re.fullmatch(r'[a-z]+_[a-z]+', text)))


#4 Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re

text = input()
print(re.findall(r'[A-Z][a-z]+', text))

#5 Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'
import re

text = input()
print(bool(re.fullmatch(r'a.*b', text)))

#6 Write a Python program to replace all occurrences of space, comma, or dot with a colon.

import re

text = input()
print(re.sub(r'[ ,.]', ':', text))


#7 Write a python program to convert snake case string to camel case string.
import re
def snake_camel(s):
    res = ''
    res += (s.group(1)).upper()
    return res

str = input()
camel = re.sub(r'(_[a-z])', snake_camel, str)
camel = camel.replace('_', '')
print(camel)


#8 Write a Python program to split a string at uppercase letters.
import re
text = input()
x = re.split('[A-Z]', text)
print(x)

#9 Write a Python program to insert spaces between words starting with capital letters
import re
def space(x):
    return ' '.join(re.findall('[A-Z][a-z]*', x))
x = input()
y = space(x)
print(y)  


#10 Write a Python program to convert a given camel case string to snake case.
import re
def com(s):
    res = ''
    if s.group(1):
        res += (s.group(1)).lower()
    else:
        res += ('_' + s.group(2)).lower()
    return res
s = input()
snake = re.sub(r'(^[A-Z]| [A-Z])|([A-Z])', com, s) 
print(snake)