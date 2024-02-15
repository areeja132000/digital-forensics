import sys

with open(sys.argv[1], "rb") as file:
    data = file.read()
print(data[:4].hex().upper())
print(data[-2:].hex().upper())