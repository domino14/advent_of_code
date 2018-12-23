from collections import defaultdict

from get_data import get_data

acres = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

acres = get_data(18)

sp = [acreline for acreline in acres.split('\n') if acreline]
world_map = defaultdict(lambda: defaultdict(lambda: '.'))

ymax = len(sp)
xmax = len(sp[0])

for y, ln in enumerate(sp):
    for x, ch in enumerate(ln):
        world_map[y][x] = ch


def printable_map(world_map):
    strs = []
    for y in range(ymax):
        arr = []
        for x in range(xmax):
            arr.append(world_map[y][x])
        strs.append(''.join(arr))
    return '\n'.join(strs)


def adjacent(world_map, x, y):
    trees = 0
    lumbers = 0
    for coord in (
        (y+1, x+1), (y+1, x), (y+1, x-1), (y, x-1), (y-1, x-1), (y-1, x),
        (y-1, x+1), (y, x+1)
            ):
        if world_map[coord[0]][coord[1]] == '|':
            trees += 1
        elif world_map[coord[0]][coord[1]] == '#':
            lumbers += 1

    return trees, lumbers


def resources(world_map):
    woods = 0
    lumbers = 0
    for rownum, row in world_map.items():
        for colnum, resource in row.items():
            if resource == '|':
                woods += 1

            elif resource == '#':
                lumbers += 1

    return woods, lumbers


print(printable_map(world_map))
for minute in range(10):
    new_world_map = defaultdict(lambda: defaultdict(lambda: '.'))
    for y in range(ymax):
        for x in range(xmax):
            adj_trees, adj_lumber = adjacent(world_map, x, y)
            if world_map[y][x] == '.':
                if adj_trees >= 3:
                    new_world_map[y][x] = '|'
                else:
                    new_world_map[y][x] = '.'
            elif world_map[y][x] == '|':
                if adj_lumber >= 3:
                    new_world_map[y][x] = '#'
                else:
                    new_world_map[y][x] = '|'
            elif world_map[y][x] == '#':
                if adj_lumber >= 1 and adj_trees >= 1:
                    new_world_map[y][x] = '#'
                else:
                    new_world_map[y][x] = '.'
    world_map = new_world_map
    # if minute % 1000 == 0:
    print(minute, '...')
    # print(printable_map(world_map))
    woods, lumbers = resources(world_map)
    print(woods, lumbers, woods*lumbers)


woods, lumbers = resources(world_map)

print(woods, lumbers, woods * lumbers)


# part 2 loops every 28
# 2569: 203814
print((1000000000 - 2569) % 28)
# answer was 27; so i looked at the loop of values and picked the 27th
# one (right above 203814) -- this value was 211653
