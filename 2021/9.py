input = open("/Users/cesar/09/input.txt", "r").readlines()
m = []

for line in input:
    row = []
    for c in line.strip():
        row.append(int(c))

    m.append(row)


lowpts = []
lowptlocs = []

for i in range(len(m)):
    for j in range(len(m[i])):
        # adjacent pts
        less = True
        for k in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if k[0] < 0 or k[0] >= len(m) or k[1] < 0 or k[1] >= len(m[i]):
                continue

            if m[i][j] >= m[k[0]][k[1]]:
                less = False

        if less:
            lowpts.append(m[i][j])
            lowptlocs.append((i, j))

risk = 0
for i in lowpts:
    risk += 1 + i

print(risk)


# part 2


def find_basin(m, pt, calls):
    i, j = pt
    sizes = []
    for k in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if k[0] < 0 or k[0] >= len(m) or k[1] < 0 or k[1] >= len(m[i]):
            continue

        if m[k[0]][k[1]] != 9 and m[k[0]][k[1]] > m[i][j]:
            calls[k] = True
            find_basin(m, k, calls)


sizes = []

for l in lowptlocs:
    calls = {l: True}
    find_basin(m, l, calls)
    sizes.append(len(calls))

prod = 1
print(sorted(sizes))
for s in list(reversed(sorted(sizes)))[:3]:
    prod *= s

print(prod)