from collections import Counter
from copy import deepcopy

input = open("./14/input.txt", "r").readlines()
tpl = input[0].strip()

rules = [r.strip() for r in input[2:]]

nr = []

for r in rules:
    r1, r2 = r.split(" -> ")
    nr.append((r1, r2))


replacements = []
pairs = {}

for idx, r in enumerate(tpl):
    pair = tpl[idx : idx + 2]
    if len(pair) != 2:
        continue
    pairs[pair] = pairs.get(pair, 0) + 1


letterct = Counter(tpl)


def mml(ctr):
    c = ctr.most_common()
    return c[0][1] - c[-1][1]


for step in range(40):
    if step == 10:
        print("p1:", mml(letterct))

    new_pairs = deepcopy(pairs)
    decrements = {}
    for r in nr:
        if pairs.get(r[0]):
            ct = pairs[r[0]]
            repl1 = r[0][0] + r[1]
            repl2 = r[1] + r[0][1]
            letterct[r[1]] += ct
            new_pairs[repl1] = new_pairs.get(repl1, 0) + ct
            new_pairs[repl2] = new_pairs.get(repl2, 0) + ct
            decrements[r[0]] = decrements.get(r[0], 0) + ct

    pairs.update(new_pairs)
    for decr, n in decrements.items():
        pairs[decr] -= n

print("p2:", mml(letterct))
