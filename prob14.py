from get_data import get_data

pzl_in = 147061

scoreboard = [3, 7]

elves = [0, 1]  # positions in scoreboard for elves 1 & 2
elf_turn = 0


def gen_new_recipes():
    # print(f'{scoreboard} {elves[0]} {elves[1]}')
    s = scoreboard[elves[0]] + scoreboard[elves[1]]
    x, y = divmod(s, 10)
    if x == 0:
        scoreboard.append(y)
    else:
        scoreboard.extend([x, y])


def process():
    num_recipes = 147061
    while True:
        gen_new_recipes()
        # print(f'Old {elves[0]} {elves[1]}')
        elves[0] = (1 + elves[0] + scoreboard[elves[0]]) % len(scoreboard)
        elves[1] = (1 + elves[1] + scoreboard[elves[1]]) % len(scoreboard)
        # print(f'New {elves[0]} {elves[1]}')
        # part 1:
        # if len(scoreboard) >= num_recipes + 10:
        #     print(''.join(str(x) for x in scoreboard[
        #         num_recipes:num_recipes+10]))
        #     break
        if ''.join([
            str(x) for x in scoreboard[-len(str(num_recipes)):]]) == str(
                num_recipes):
            print(f'part 2: {len(scoreboard)-len(str(num_recipes))}')
            break
        if len(scoreboard) % 10000 == 1:
            print(f'{len(scoreboard)}..')


if __name__ == '__main__':
    process()  # part1
