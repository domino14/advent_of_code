players = 432
last_marble_pts = 71019*100

scores = [0] * players
marble_layout = [0]

current_marble_idx = 0


def place_new_marble(marble, scores, cur_player):
    global current_marble_idx
    global marble_layout
    # print(f'Marble {marble}, cur_player {cur_player}')
    # otherwise, use existing marble
    if marble % 23 != 0:
        new_place = current_marble_idx + 2
        if new_place > len(marble_layout):
            new_place = new_place - len(marble_layout)
        marble_layout.insert(new_place, marble)
        current_marble_idx = new_place
        # print(f'layout meow: {marble_layout}, cur_marble_idx '
        #       f'{current_marble_idx}')
    else:
        # remove marble 7 spaces ccw
        to_remove = current_marble_idx - 7
        if to_remove < 0:
            to_remove = len(marble_layout) + to_remove
        marble_at = marble_layout[to_remove]
        # Add marble we woulda placed, and the marble at the square
        scores[cur_player-1] += marble + marble_at
        #print(f'removing marble {marble_at} (idx {to_remove})')
        marble_layout = marble_layout[:to_remove] + marble_layout[to_remove+1:]
        current_marble_idx = to_remove
        # print(f'layout meow: {marble_layout}, cur_marble_idx '
        #       f'{current_marble_idx}')


cur_player = 0
for i in range(1, last_marble_pts+1):
    cur_player += 1
    if cur_player == players + 1:
        cur_player = 1
    place_new_marble(i, scores, cur_player)
    if i % 10000 == 0:
        print(f'...{i}')
print(f'ans {max(scores)}')
