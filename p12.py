from collections import defaultdict
from get_data import get_data, get_data_lines


state = defaultdict(lambda: '.')

lines = get_data_lines(12)

# lines = """initial state: #..#.#..##......###...###
# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #""".split('\n')

initial_state = lines[0].split(': ')[1]

for idx, c in enumerate(initial_state):
    state[idx] = c

transitions = lines[1:]

trans_dict = {}
for transition in transitions:
    config, result = transition.split(' => ')
    trans_dict[config] = result

print(state)


def printable_state(state):
    s = ''
    for i in range(-3, 36):
        s += state[i]
    return s


def calc_sum(state):
    s = 0
    for k, v in state.items():
        if v == '#':
            s += k
    return s


for gen in range(1, 501):
    new_state = defaultdict(lambda: '.')
    left_start = min(state.keys()) - 5
    # print('starting at ', left_start)
    for i in range(len(state) + 10):
        # Start looking left.
        j = left_start + i
        key = f'{state[j]}{state[j+1]}{state[j+2]}{state[j+3]}{state[j+4]}'
        if key in trans_dict:
            new_state[j+2] = trans_dict[key]

    state = new_state
    # print(printable_state(state))
    # if gen % 1000 == 0:

    print(f'Generation {gen}, sum={calc_sum(state)}')


# seems to converge to adding 22 every iteration.
# Generation 500, sum=11475

LIMIT = 50000000000
print((LIMIT - 500) * 22 + 11475)