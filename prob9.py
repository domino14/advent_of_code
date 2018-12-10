players = 432
last_marble_pts = 71019*100


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def next_ct(self, n):
        nn = self
        for i in range(n):
            nn = nn.next
        return nn

    def previous_ct(self, n):
        pn = self
        for i in range(n):
            pn = pn.previous
        return pn

    def make_next(self, node):
        self.next = node
        node.previous = self

    def print_layout(self):
        start = self
        next = start.next
        values = [self.value]
        while next.value != start.value:
            values.append(next.value)
            next = next.next_ct(1)
        print(' '.join([str(v) for v in values]))


scores = [0] * players
initial_marble = Marble(0)
initial_marble.make_next(initial_marble)
current_marble_node = initial_marble


def place_new_marble(marble, scores, cur_player):
    global current_marble_node
    # print(f'Marble {marble}, cur_player {cur_player}')
    # otherwise, use existing marble
    if marble % 23 != 0:
        placeholder = current_marble_node.next_ct(2)
        placeholder_previous = current_marble_node.next_ct(1)
        new_node = Marble(marble)
        placeholder_previous.make_next(new_node)
        new_node.make_next(placeholder)

        current_marble_node = new_node
    else:
        # remove marble 7 spaces ccw
        to_remove = current_marble_node.previous_ct(7)
        scores[cur_player - 1] += marble + to_remove.value

        to_remove_prev = current_marble_node.previous_ct(8)
        to_remove_prev.make_next(to_remove.next)
        current_marble_node = to_remove.next

    # current_marble_node.print_layout()


cur_player = 0
for i in range(1, last_marble_pts+1):
    cur_player += 1
    if cur_player == players + 1:
        cur_player = 1
    place_new_marble(i, scores, cur_player)
    if i % 10000 == 0:
        print(f'...{i}')
print(f'ans {max(scores)}')
