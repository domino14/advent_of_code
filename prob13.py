from get_data import get_data, get_data_lines

DIR_L = 0
DIR_U = 1
DIR_R = 2
DIR_D = 3
cart_markers = set(['>', '^', '<', 'v'])


class Cart:
    def __init__(self, cart_id, x, y, facing):
        self.x = x
        self.y = y
        self.cart_id = cart_id
        self.facing = facing
        self.next_turn = DIR_L
        self.crashed = False

    def turn(self, dir):
        """ turn in a direction (left or right) """
        if dir == DIR_L:
            self.facing = (self.facing - 1) % 4
        elif dir == DIR_R:
            self.facing = (self.facing + 1) % 4

    def __str__(self):
        if self.facing == DIR_L:
            return '<'
        if self.facing == DIR_R:
            return '>'
        if self.facing == DIR_U:
            return '^'
        if self.facing == DIR_D:
            return 'v'

    def crash(self, carts):
        for cart in carts:
            if cart.x == self.x and cart.y == self.y and cart.cart_id != self.cart_id:
                cart.crashed = True
                self.crashed = True
                print(f'Crash occurred at {self.x}, {self.y}!')

    def travel(self, tracks, carts):
        if self.crashed:
            return  # Done traveling
        if self.facing == DIR_L:
            self.x = self.x - 1
            next = tracks[self.y][self.x]
            if next == '\\':
                self.turn(DIR_R)
            if next == '/':
                self.turn(DIR_L)
            if next == '+':
                self.turn(self.next_turn)
                self.next_turn = (self.next_turn + 1) % 3
            self.crash(carts)

        elif self.facing == DIR_U:
            self.y = self.y - 1
            next = tracks[self.y][self.x]
            if next == '/':
                self.turn(DIR_R)
            if next == '\\':
                self.turn(DIR_L)
            if next == '+':
                self.turn(self.next_turn)
                self.next_turn = (self.next_turn + 1) % 3
            self.crash(carts)

        elif self.facing == DIR_R:
            self.x = self.x + 1
            next = tracks[self.y][self.x]
            if next == '\\':
                self.turn(DIR_R)
            if next == '/':
                self.turn(DIR_L)
            if next == '+':
                self.turn(self.next_turn)
                self.next_turn = (self.next_turn + 1) % 3
            self.crash(carts)

        elif self.facing == DIR_D:
            self.y = self.y + 1
            next = tracks[self.y][self.x]
            if next == '/':
                self.turn(DIR_R)
            if next == '\\':
                self.turn(DIR_L)
            if next == '+':
                self.turn(self.next_turn)
                self.next_turn = (self.next_turn + 1) % 3
            self.crash(carts)


raw_data = list(filter(lambda ln: ln.strip() != '', r"""
/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
      """.split('\n')))

raw_data = get_data_lines(13)

tracks = []
carts = []
cart_id = 1
for y, line in enumerate(raw_data):
    tracks.append(list(line))
    for idx, c in enumerate(list(line)):
        cart_dir = None
        if c == 'v':
            cart_dir = DIR_D
            tracks[y][idx] = '|'
        if c == '^':
            cart_dir = DIR_U
            tracks[y][idx] = '|'
        if c == '>':
            cart_dir = DIR_R
            tracks[y][idx] = '-'
        if c == '<':
            cart_dir = DIR_L
            tracks[y][idx] = '-'
        if cart_dir is not None:
            cart = Cart(cart_id, idx, y, cart_dir)
            carts.append(cart)
            cart_id += 1


def print_track():
    for y, track in enumerate(tracks):
        to_print = list(''.join(track))
        for cart in carts:
            if cart.y == y:
                to_print[cart.x] = str(cart)

        print(''.join(to_print))

    print()


def tick():
    for cart in sorted(carts, key=lambda c: c.y * 1000 + c.x):
        cart.travel(tracks, carts)


print_track()
tick_ct = 0
while True:
    tick()
    tick_ct += 1
    carts_copy = []
    for cart in carts:
        if not cart.crashed:
            carts_copy.append(cart)

    carts = carts_copy
    # print_track()
    if len(carts) == 1:
        print(carts[0].x, carts[0].y)
        print(f'{tick_ct} ticks')
        break

