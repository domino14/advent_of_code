from get_data import get_data_lines
from collections import defaultdict

data = get_data_lines(6)

new_data = []
idx = 0
for coords in data:
    new_data.append([idx, *[int(i) for i in coords.split(',')]])
    idx += 1

# Make a big grid
GRID_SIZE = 400
OUTLINE_SIZE = 1200

grid = []
for i in range(GRID_SIZE):
    grid.append([None] * GRID_SIZE)


def tcd(x, y, i, j):
    return abs(x - i) + abs(y - j)


for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        # find closest pt
        closest_dist = 10000000000
        closest_pt = -1
        for idx, x, y in new_data:
            d = tcd(x, y, i, j)
            if grid[j][i] is None:
                grid[j][i] = {}
            grid[j][i][idx] = d
        items = grid[j][i].items()
        r = sorted(items, key=lambda x: x[1])
        if len(r) > 1 and r[0][1] == r[1][1]:
            grid[j][i]['closest'] = '.'
        else:
            grid[j][i]['closest'] = r[0][0]

ttl = 0
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        s = sum([y[1] for y in grid[j][i].items() if y[0] != 'closest'])
        if s < 10000:
            ttl += 1

print('part 2', ttl)

# Count areas

to_discard = set()

for tt in range(2):
    for i in range(int(-OUTLINE_SIZE/2), int(OUTLINE_SIZE/2)):
        # This is a point at "infinity". The closest point should be discarded
        # from consideration.
        closest_d1 = 100000000
        closest_pt_1 = -1
        closest_d2 = 100000000
        closest_pt_2 = -1
        for idx, x, y in new_data:
            if tt == 0:
                d1 = tcd(x, y, i, -OUTLINE_SIZE/2)
                d2 = tcd(x, y, i, OUTLINE_SIZE/2)
            else:
                d1 = tcd(x, y, -OUTLINE_SIZE/2, i)
                d2 = tcd(x, y, OUTLINE_SIZE/2, i)
            if d1 < closest_d1:
                closest_d1 = d1
                closest_pt_1 = idx
            if d2 < closest_d2:
                closest_d2 = d2
                closest_pt_2 = idx
                #     closest_pt = idx

        to_discard.add(closest_pt_1)
        to_discard.add(closest_pt_2)


areas = defaultdict(int)
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        cl = grid[j][i]['closest']
        if cl != '.' and cl not in to_discard:
            areas[cl] += 1


print("part 1", sorted(areas.items(), key=lambda y: -y[1])[0][1])
