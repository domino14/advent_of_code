from collections import defaultdict, namedtuple

mx, my = 0, 0
# depth, tx, ty = 6084, 14, 709

depth, tx, ty = 510, 10, 10

bfsxmul, bfsymul = 12, 1.2

State = namedtuple('State', ['x', 'y', 'equipped'])

TORCH = 'torch'
CLIMBING = 'climbing'

# y then x
erosion_level_map = defaultdict(lambda: defaultdict(int))
cave_system_map = defaultdict(lambda: defaultdict(lambda: '?'))


def geo_idx(x, y):
    if x == 0 and y == 0:
        return 0
    if x == tx and y == ty:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion_level(x-1, y) * erosion_level(x, y-1)


def erosion_level(x, y):
    if y in erosion_level_map:
        if x in erosion_level_map[y]:
            return erosion_level_map[y][x]
    # otherwise calculate
    el = (geo_idx(x, y) + depth) % 20183
    erosion_level_map[y][x] = el
    return el


def create_map():
    # Create a map from mx, my to tx, ty, but precalculate more cells.
    for y in range(my, int(ty * bfsymul + 1)):
        for x in range(mx, int(tx * bfsxmul + 1)):
            cave_system_map[y][x] = region_type(x, y)


def region_type(x, y):
    el = erosion_level(x, y)
    if el % 3 == 0:
        return '.'
    elif el % 3 == 1:
        return '='
    elif el % 3 == 2:
        return '|'


def cell_at_map(x, y):
    if cave_system_map[y][x] != '?':
        return cave_system_map[y][x]
    # Otherwise generate it
    print(f'Cell at map did not exist, generating: {x} {y}')
    el = region_type(x, y)
    cave_system_map[y][x] = el
    return el


def printable_map():
    strs = []
    for y in range(15):
        arr = []
        for x in range(15):
            arr.append(cave_system_map[y][x])
        strs.append(''.join(arr))
    return '\n'.join(strs)


def calculate_risk(tlx, tly, brx, bry):
    risk = 0

    def risk_for_type(t):
        return {
            '.': 0,
            '=': 1,
            '|': 2,
        }[t]

    for y in range(tly, bry + 1):
        for x in range(tlx, brx + 1):
            risk += risk_for_type(cave_system_map[y][x])

    return risk


def equipment_permitted(cell):
    return {
        '.': [TORCH, CLIMBING],
        '=': [CLIMBING, None],
        '|': [TORCH, None],
    }[cell]


def queue_addition(orig_state, orig_cost):
    """ Add a bunch of points with different states to an array and
        return that array.
    """
    # The four closest cells, with all combinations of removing / adding
    # equipment (if possible)
    my_region = cell_at_map(orig_state.x, orig_state.y)
    my_equipped = orig_state.equipped
    to_add = []
    for cell in [(orig_state.x + 1, orig_state.y),
                 (orig_state.x, orig_state.y + 1),
                 (orig_state.x - 1, orig_state.y),
                 (orig_state.x, orig_state.y - 1)]:
        # Shouldn't need this much space, but need to leave a buffer.
        if (cell[0] < 0 or cell[1] < 0 or cell[0] > tx * bfsxmul or
                cell[1] > ty * bfsymul):
            continue
        cell_region = cell_at_map(cell[0], cell[1])
        # our BFS is backwards so we need to determine equipment from
        # cell_region to here.
        if my_equipped not in equipment_permitted(cell_region):
            # Need to switch equipment before arriving here.
            for permitted in equipment_permitted(cell_region):
                # 8 is 7 to change equipment + 1 for the move.
                state_to_add, cost = (State(cell[0], cell[1], permitted),
                                      8 + orig_cost)
                to_add.append((state_to_add, cost))
        else:
            # There's no need to pre-emptively change equipment in the middle
            # of a path (or rather it won't make a difference if we wait until
            # the last minute, which is what we do in the case above)
            # XXX: maybe it does?
            for permitted in equipment_permitted(my_region):
                state_to_add, cost = (State(cell[0], cell[1], permitted),
                                      1 + orig_cost if permitted == my_equipped
                                      else 8 + orig_cost)
                to_add.append((state_to_add, cost))
    # Finally, add different equipment combinations for current cell.
    permitted = equipment_permitted(my_region)
    for eq in permitted:
        if eq == my_equipped:
            continue
        state_to_add, cost = (State(orig_state.x, orig_state.y, eq),
                              7 + orig_cost)
        to_add.append((state_to_add, cost))
    return to_add


def bfs(beginning, end):
    endstate = State(end[0], end[1], 'torch')
    cost = 0
    queue = [(endstate, cost)]
    lookup_queue = {}

    el_idx = -1

    while el_idx < len(queue) - 1:
        el_idx += 1
        state, cost = queue[el_idx]
        # look at four closest cells, including equipment changes.
        # also look at current cell with equipment changes.
        to_add = queue_addition(state, cost)
        # print(f'Got from queue: {state}, {cost} -- adding {to_add}')
        to_add_copy = []
        for new_state, calculated_cost in to_add:
            remove = False
            # Search the queue to see if this cell already exists with a lower
            # cost than the `calculated_cost`
            existing_cost = lookup_queue.get((new_state.x, new_state.y,
                                              new_state.equipped))

            if existing_cost is not None and existing_cost <= calculated_cost:
                remove = True

            if not remove:
                to_add_copy.append((new_state, calculated_cost))

        queue.extend(to_add_copy)
        for el in to_add_copy:
            lookup_queue[(el[0].x, el[0].y, el[0].equipped)] = el[1]
        if el_idx % 10000 == 0:
            print(f'Processed {el_idx} cells... (sample {state}, {cost}, '
                  f'{len(to_add_copy)}')
    # bfs is complete.
    # Torch is equipped at the beginning:
    return lookup_queue[(beginning[0], beginning[1], TORCH)]


if __name__ == '__main__':
    create_map()
    # print(printable_map())
    risk = calculate_risk(mx, my, tx, ty)
    print(f'Part 1: {risk}')
    min_time = bfs([mx, my], [tx, ty])
    print(f'Part 2: {min_time}')  # 951 is too low
