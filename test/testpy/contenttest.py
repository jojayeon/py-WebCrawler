content = "Python is great. I love Python. Python is versatile."
term = "python"

# 대소문자 변환 후 빈도 계산
a = term.lower()
print(a)
b = content.lower()
print(b)
c = b.count(a)
print(c)

frequency = content.lower().count(term.lower())
print(frequency)