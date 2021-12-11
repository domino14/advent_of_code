input = open("/Users/cesar/11/input.txt", "r").readlines()


m = []
for row in input:
    r = []
    for c in row.strip():
        r.append(int(c))

    m.append(r)


def diag_adj(m, row, column):
    pts = [
        (row + 1, column),
        (row - 1, column),
        (row, column + 1),
        (row, column - 1),
        (row + 1, column + 1),
        (row + 1, column - 1),
        (row - 1, column + 1),
        (row - 1, column - 1),
    ]

    actual = []

    for p in pts:
        if p[0] < 0 or p[0] >= len(m):
            continue
        if p[1] < 0 or p[1] >= len(m[p[0]]):
            continue
        actual.append(p)
    return actual


num_flashes = 0


def flash(m, ridx, cidx, flashed):
    if (ridx, cidx) in flashed:
        return
    global num_flashes
    num_flashes += 1
    flashed.add((ridx, cidx))
    d = diag_adj(m, ridx, cidx)
    for (r, c) in d:
        m[r][c] += 1
        if m[r][c] > 9:
            flash(m, r, c, flashed)


def st(m):
    # run a step
    for ridx, row in enumerate(m):
        for cidx, c in enumerate(row):
            m[ridx][cidx] += 1

    flashed = set()

    for ridx, row in enumerate(m):
        for cidx, c in enumerate(row):
            if c > 9:
                # flash
                flash(m, ridx, cidx, flashed)

    for pt in flashed:
        m[pt[0]][pt[1]] = 0


step = 0
while True:
    st(m)
    step += 1
    if step == 100:
        print("part 1:", num_flashes)
    all_0 = True
    for ridx, row in enumerate(m):
        for cidx, c in enumerate(row):
            if c != 0:
                all_0 = False
                break

    if all_0:
        print("part 2:", step)
        break
