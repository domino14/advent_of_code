from collections import defaultdict
from get_data import get_data


maxx = -10000000
maxy = maxx
minx = 10000000
miny = minx

nodes = {}


class RoomNode:
    # y increases from top to bottom
    def __init__(self, x, y):
        global maxx, maxy, minx, miny
        self.N = None
        self.E = None
        self.S = None
        self.W = None
        self.x = x
        self.y = y
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        nodes[(x, y)] = self
        self.cost_to_visit = 0

    def __repr__(self):
        return f'<RoomNode: ({self.x}, {self.y})>'

    def next_room_loc(self, direction):
        if direction == 'N':
            return (self.x, self.y - 2)
        elif direction == 'E':
            return (self.x + 2, self.y)
        elif direction == 'S':
            return (self.x, self.y + 2)
        elif direction == 'W':
            return (self.x - 2, self.y)


def opposite(dir):
    return {
        'N': 'S',
        'E': 'W',
        'S': 'N',
        'W': 'E',
    }[dir]


def parse_regex(regex, parent):
    regex = regex.replace('^', '').replace('$', '')
    skip_until = None
    first_parent = parent
    for idx, el in enumerate(regex):
        if skip_until and idx < skip_until:
            continue
        if el in ('N', 'E', 'S', 'W'):
            x, y = parent.next_room_loc(el)
            if (x, y) not in nodes:
                new_room = RoomNode(x, y)
            else:
                new_room = nodes[(x, y)]
            setattr(parent, el, new_room)
            setattr(new_room, opposite(el), parent)
            # print(f'Set {parent} and {new_room} to point to each other.')
            if not new_room.cost_to_visit:
                new_room.cost_to_visit += parent.cost_to_visit + 1
            parent = new_room
        elif el == '(':
            # find closing paren
            ct = 0
            for ridx, rel in enumerate(regex[idx:]):
                if rel == '(':
                    ct += 1
                elif rel == ')':
                    ct -= 1
                if ct == 0:
                    ridx = ridx + idx
                    break
            # print(f'Parsing subregex: {regex[idx + 1:ridx]}')
            parse_regex(regex[idx + 1:ridx], parent)
            skip_until = ridx + 1
        elif el == '|':
            parent = first_parent


def traverse_map(node, base_map):
    if not node:
        return

    if node.N:
        base_map[node.y - 1][node.x] = '-'
        if base_map[node.N.y][node.N.x] != '.':
            base_map[node.N.y][node.N.x] = '.'
            traverse_map(node.N, base_map)
    else:
        base_map[node.y - 1][node.x] = '#'

    if node.E:
        base_map[node.y][node.x + 1] = '|'
        if base_map[node.E.y][node.E.x] != '.':
            base_map[node.E.y][node.E.x] = '.'
            traverse_map(node.E, base_map)
    else:
        base_map[node.y][node.x + 1] = '#'

    if node.S:
        base_map[node.y + 1][node.x] = '-'
        if base_map[node.S.y][node.S.x] != '.':
            base_map[node.S.y][node.S.x] = '.'
            traverse_map(node.S, base_map)
    else:
        base_map[node.y + 1][node.x] = '#'

    if node.W:
        base_map[node.y][node.x - 1] = '|'
        if base_map[node.W.y][node.W.x] != '.':
            base_map[node.W.y][node.W.x] = '.'
            traverse_map(node.W, base_map)
    else:
        base_map[node.y][node.x - 1] = '#'


def print_map(base_map):
    strs = []
    for y in range(miny - 1, maxy + 2):
        arr = []
        for x in range(minx - 1, maxx + 2):
            arr.append(base_map[y][x])
        strs.append(''.join(arr))
    printable = '\n'.join(strs)
    print(printable)


def determine_furthest_room(nodes, parent):
    max_path_length = 0
    thousand_doors = 0
    for _, node in nodes.items():
        path_length = node.cost_to_visit
        if path_length > max_path_length:
            max_path_length = path_length
        if path_length >= 1000:
            thousand_doors += 1
    print(f'Furthest room: {max_path_length}')
    print(f'Thousand doors: {thousand_doors}')


def traverse_and_print_map(parent):
    # y, then x
    base_map = defaultdict(lambda: defaultdict(lambda: '#'))
    print(maxx, minx, maxy, miny)
    traverse_map(parent, base_map)
    base_map[1000][1000] = 'X'
    print_map(base_map)


if __name__ == '__main__':
    regex = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
    # Start ourselves at 1000, 1000
    regex = get_data(20)
    parent = RoomNode(1000, 1000)
    parse_regex(regex, parent)

    print(len(nodes), 'nodes')
    # traverse_and_print_map(parent)
    determine_furthest_room(nodes, parent)
