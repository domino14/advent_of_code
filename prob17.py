from collections import defaultdict
from get_data import get_data_lines
from PIL import Image
import uuid
WATER_LOC = (500, 0)


recursed = {}

def create_map(lines):
    # map -- y, then x
    min_y = 1000000
    min_x = 1000000
    max_y = -1000000
    max_x = -1000000
    map = defaultdict(lambda: defaultdict(lambda: '.'))
    map[WATER_LOC[1]][WATER_LOC[0]] = '+'

    for line in lines:
        coords = line.split(', ')
        vein = []
        for coord in coords:
            a, num = coord.split('=')
            vein.append((a, num))

        if vein[0][0] == 'x':
            assert vein[1][0] == 'y'
            ystart, yend = [int(i) for i in vein[1][1].split('..')]
            if ystart < min_y:
                min_y = ystart
            if yend > max_y:
                max_y = yend
            x = int(vein[0][1])
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            for y in range(ystart, yend+1):
                map[y][x] = '#'

        if vein[0][0] == 'y':
            assert vein[1][0] == 'x'
            xstart, xend = [int(i) for i in vein[1][1].split('..')]
            y = int(vein[0][1])
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

            if xstart < min_x:
                min_x = xstart
            if xend > max_x:
                max_x = xend

            for x in range(xstart, xend+1):
                map[y][x] = '#'

    return map, min_x, max_x, min_y, max_y


def print_map(map, min_y, max_y):
    # These can be varied for debugging.
    x_min = 475
    x_max = 525
    strs = []
    for y in range(min_y, max_y+1):
        arr = []
        for x in range(x_min, x_max+1):
            arr.append(map[y][x])
        strs.append(''.join(arr))

    return '\n'.join(strs)


def trace_drop_path(map, min_y, max_y, x, y, drops_gen):

    # settled = False
    while y < max_y:
        # if not move_horizontal:
        x, y = x, y + 1

        if map[y][x] in ('.', '|'):
            # drop through
            map[y][x] = '|'
            # print(f'Dropping through x={x} y={y}')
        else:
            # It's either ~ or #. Travel left and right and bounce back.
            # First subdrop goes left, bounces back, and stops when it hits
            # a point we have already seen TWICE (or goes off the edge).
            # Second subdrop goes right, bounces back, and stops when it hits
            # a point we hve already seen TWICE (or goes off the edge).
            # IF the two points are in the same Y, pick the farthest from
            # x = 500
            #
            # print(f'Was {map[y][x]}, moving sideways on y={y-1}')
            s1x, s1y = move_sideways(map, min_y, max_y, x, y-1, -1, drops_gen)
            s2x, s2y = move_sideways(map, min_y, max_y, x, y-1, 1, drops_gen)

            # XXX: Note this is potentially an issue:
            if s1x != -1 and s2x != -1 and s1y == s2y:
                ysettle = s1y
                locs = sorted([s1x, s2x, WATER_LOC[0]])
                if locs[0] == WATER_LOC[0]:
                    xsettle = locs[2]
                elif locs[2] == WATER_LOC[0]:
                    xsettle = locs[0]
                else:
                    xsettle = locs[0]

                # print(f'Settling at {xsettle, ysettle}')
                map[ysettle][xsettle] = '~'
            break
        # if drops_gen == 1281 and y > 1900:
        #     save_image(map, min_x, max_x, min_y, max_y,
        #                f'drops_{drops_gen}_{uuid.uuid4()}.png')


def move_sideways(map, min_y, max_y, x, y, dir, drops_gen):
    still_moving_sideways = True
    seen_map = defaultdict(int)

    while still_moving_sideways:
        x += dir

        # print(f'In move sideways, testing {x}, {y}')
        if map[y][x] in ('.', '|'):
            map[y][x] = '|'
            # print(f'Setting to |, cuz x={x} and y={y}')
            if map[y+1][x] in ('.', '|'):
                # print(f'Tracing drop path again, since {x}, {y+1} was sand')
                if (x, y) not in recursed:
                    trace_drop_path(map, min_y, max_y, x, y, drops_gen)
                recursed[(x, y)] = True
                still_moving_sideways = False
                return -1, -1
        else:
            # It's a wall or drop,  bounce back.
            # print(f'Bounce back bounce back bounce back')
            x -= dir
            dir *= -1
        # elif map[y][x] == '~':
        #     # If we bump sideways into a drop, settle down before we bump.
        #     print(f'Bumped into a drop at {x},{y}, settle at {x-dir},{y}')
        #     return (x - dir, y)

        seen_map[(x, y)] += 1
        if seen_map[(x, y)] == 2:
            return x, y

    return -1, -1


def save_image(map, min_x, max_x, min_y, max_y, name):
    colors = []
    rgb_lookup = {
        '+': [133, 255, 218],
        '~': [62, 200, 242],
        '|': [247, 210, 46],
        '#': [135, 79, 20],
        '.': [186, 170, 154],
    }
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            rgb = rgb_lookup[map[y][x]]
            colors.extend(rgb)

    colors = bytes(colors)
    img = Image.frombytes('RGB', ((max_x - min_x + 1), (max_y - min_y + 1)),
                          colors)
    img.save(name)


def count_water(map):
    settled_ct = 0
    sand_ct = 0
    for x, ys in map.items():
        for y, tileval in ys.items():
            if tileval == '~':
                settled_ct += 1
            elif tileval == '|':
                sand_ct += 1
    return settled_ct, sand_ct


if __name__ == '__main__':
    lines = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".split('\n')

    lines = get_data_lines(17)

    map, min_x, max_x, min_y, max_y = create_map(lines)
    print(f'min_y={min_y}, max_y={max_y}, min_x={min_x}, max_x={max_x}')
    last_settled_ct, last_sand_ct = None, None
    drops_gen = 0
    while True:
        recursed = {}
        print('--------------')
        x, y = WATER_LOC
        trace_drop_path(map, min_y, max_y, x, y, drops_gen)

        settled_ct, sand_ct = count_water(map)
        if (settled_ct, sand_ct) == (last_settled_ct, last_sand_ct):
            break
        last_settled_ct, last_sand_ct = settled_ct, sand_ct
        drops_gen += 1
        # if drops_gen % 10 == 0:
        print(f'{drops_gen} ({last_settled_ct, last_sand_ct})')
        # print(print_map(map, min_y, max_y))
        if drops_gen % 1000 == 0:
            save_image(map, min_x, max_x, min_y, max_y,
                       f'drops_{drops_gen}.png')
    save_image(map, min_x, max_x, min_y, max_y,
               f'drops_{drops_gen}.png')
    print(f'Part 1: {last_settled_ct + last_sand_ct} (drops={drops_gen})')
