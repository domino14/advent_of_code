input = open("/Users/cesar/02/input.txt", "r").readlines()


h = 0
v = 0
for line in input:
    d, p = line.split()
    if d == "forward":
        v += int(p)
    elif d == "down":
        h += int(p)
    elif d == "up":
        h -= int(p)

print(h * v)

## two

h = 0
v = 0
aim = 0

for line in input:
    d, p = line.split()
    if d == "forward":
        v += int(p)
        h += aim * int(p)
    elif d == "down":
        aim += int(p)
    elif d == "up":
        aim -= int(p)

print(h * v)
