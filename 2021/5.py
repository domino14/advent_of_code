input = open("/Users/cesar/05/input.txt", "r").readlines()


def solve(hv=False):
    mp = {}
    for line in input:
        a = line.split("->")
        x1, y1 = [int(n) for n in a[0].split(",")]
        x2, y2 = [int(n) for n in a[1].split(",")]

        if x1 == x2:
            for i in range(min(y1, y2), max(y1, y2) + 1):
                c = (x1, i)
                if c in mp:
                    mp[c] += 1
                else:
                    mp[c] = 1
        elif y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                c = (i, y1)
                if c in mp:
                    mp[c] += 1
                else:
                    mp[c] = 1
        elif not hv:
            # diagonal
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            for i in range(x1, x2 + 1):
                if y2 > y1:
                    j = y1 + (i - x1)
                else:
                    j = y1 - (i - x1)
                c = (i, j)
                if c in mp:
                    mp[c] += 1
                else:
                    mp[c] = 1

    ct = 0
    for i in mp:
        if mp[i] > 1:
            ct += 1

    print(ct)


# 1
solve(True)
# 2
solve(False)