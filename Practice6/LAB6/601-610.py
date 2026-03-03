#1
n = int(input())
numbers = list(map(int, input().split()))

squares = map(lambda x: x**2, numbers)

print(sum(squares))

#2
n = int(input())
numbers = list(map(int, input().split()))

even_numbers = filter(lambda x: x % 2 == 0, numbers)

print(len(list(even_numbers)))

#3
n = int(input())
words = input().split()

for index, word in enumerate(words):
    print(f"{index}:{word}", end=" ")

#4
n = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

result = sum(a * b for a, b in zip(A, B))

print(result)

#5
s = input()

vowels = "aeiou"

if any(char.lower() in vowels for char in s):
    print("Yes")
else:
    print("No")

#6
n = int(input())
numbers = list(map(int, input().split()))

if all(x >= 0 for x in numbers):
    print("Yes")
else:
    print("No")

#7
n = int(input())
words = input().split()

longest = max(words, key=len)

print(longest)

#8
n = int(input())
numbers = list(map(int, input().split()))

unique_sorted = sorted(set(numbers))

print(*unique_sorted)

#9
n = int(input())

keys = input().split()
values = input().split()

data = dict(zip(keys, values))

query = input()

print(data.get(query, "Not found"))

#10
n = int(input())
numbers = map(int, input().split())

truthy_count = sum(map(bool, numbers))

print(truthy_count)