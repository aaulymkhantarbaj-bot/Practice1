#1
import re

text = "My phone number is 87071234567"

pattern = r"\d+"   # найти числа
result = re.search(pattern, text)

if result:
    print("Found:", result.group())

#2
import re

text = "cat bat mat"

# .  → любой символ
print(re.findall(r"c.t", text))

# *  → 0 или больше
print(re.findall(r"ca*t", "ct cat caaat"))

# +  → 1 или больше
print(re.findall(r"ca+t", "ct cat caaat"))

# ?  → 0 или 1
print(re.findall(r"colou?r", "color colour"))

# ^  → начало строки
print(re.findall(r"^cat", "cat is here"))

# $  → конец строки
print(re.findall(r"here$", "come here"))

# [] → набор символов
print(re.findall(r"[cb]at", text))

# | → или
print(re.findall(r"cat|bat", text))

# () → группировка
print(re.findall(r"(ca)t", "cat"))

# \ → экранирование
print(re.findall(r"\.", "file.txt"))

#3
import re

text = "User123 email@test.com"

print(re.findall(r"\d+", text))   # цифры
print(re.findall(r"\w+", text))   # слова
print(re.findall(r"\s", text))    # пробелы

print(re.findall(r"\D+", text))   # не цифры
print(re.findall(r"\W+", text))   # не буквы/цифры
print(re.findall(r"\S+", text))   # не пробелы

print(re.findall(r"\AUser", text))  # начало строки
print(re.findall(r"com\Z", text))   # конец строки

#4
import re

text = "abc123XYZ"

print(re.findall(r"[a-z]+", text))  # маленькие буквы
print(re.findall(r"[A-Z]+", text))  # большие буквы
print(re.findall(r"[0-9]+", text))  # цифры
print(re.findall(r"[a-zA-Z0-9]+", text))  # все вместе

#5
import re

text = "aaa aa aaaaa"

print(re.findall(r"a{2}", text))     # ровно 2
print(re.findall(r"a{2,}", text))    # 2 или больше
print(re.findall(r"a{2,4}", text))   # от 2 до 4

#6
import re

text = "Python is powerful"

match = re.search(r"power", text)

if match:
    print("Found:", match.group())


#7
import re

text = "apple banana apple"

matches = re.findall(r"apple", text)
print(matches)


#8
import re

text = "one,two;three four"

result = re.split(r"[ ,;]", text)
print(result)


#9
import re

text = "My number is 12345"

result = re.sub(r"\d+", "XXXXX", text)
print(result)

#10
import re

text = "Hello world"

match = re.match(r"Hello", text)

if match:
    print("Matched at beginning")


#11
import re

text = "Hello\nhello\nHELLO"

# IGNORECASE
print(re.findall(r"hello", text, re.IGNORECASE))

# MULTILINE
print(re.findall(r"^hello", text, re.MULTILINE | re.IGNORECASE))
