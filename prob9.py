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

scores = [0] * players

initial_marble = Marble(0)
initial_marble.next = initial_marble
initial_marble.previous = initial_marble

# marble_layout = [Marble(0)]

current_marble_node = initial_marble




def place_new_marble(marble, scores, cur_player):
    global current_marble_node
    global marble_layout
    # print(f'Marble {marble}, cur_player {cur_player}')
    # otherwise, use existing marble
    if marble % 23 != 0:
        placeholder = current_marble_node.next_ct(2)
        placeholder_previous = current_marble_node.next_ct(1)
        new_node = Marble(marble)
        placeholder_previous.next = new_node
        new_node.previous = placeholder_previous
        new_node.next = placeholder
        placeholder.previous = new_node
        current_marble_node = new_node
    else:
        # remove marble 7 spaces ccw
        # to_remove = current_marble_idx - 7
        
        # if to_remove < 0:
        #     to_remove = len(marble_layout) + to_remove
        # marble_at = marble_layout[to_remove]
        # Add marble we woulda placed, and the marble at the square
        # scores[cur_player-1] += marble + marble_at
        #print(f'removing marble {marble_at} (idx {to_remove})')
        # del marble_layout[to_remove]
        # current_marble_idx = to_remove
        # print(f'layout meow: {marble_layout}, cur_marble_idx '
        #       f'{current_marble_idx}')
        current_marble_node

cur_player = 0
for i in range(1, last_marble_pts+1):
    cur_player += 1
    if cur_player == players + 1:
        cur_player = 1
    place_new_marble(i, scores, cur_player)
    if i % 10000 == 0:
        print(f'...{i} {len(marble_layout)}')
print(f'ans {max(scores)}')
