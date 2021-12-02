input = open("/Users/cesar/01/input.txt", "r").read().strip()

last = -1000
t = 0
for l in input.split("\n"):
    n = int(l)
    if n > last:
        t += 1
    last = n


print(t - 1)

## part two

last = -1000
t = 0
lines = [int(n) for n in input.split("\n")]

for x in range(len(lines) - 2):
    three = lines[x] + lines[x + 1] + lines[x + 2]

    if three > last:
        t += 1

    last = three

print(t - 1)
