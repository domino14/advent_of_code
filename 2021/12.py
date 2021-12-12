input = open("./12/input.txt", "r").readlines()


class Cave:
    tp: str

    def __init__(self, name):
        self.tp = "small"
        if name.lower() != name:
            self.tp = "big"

        self.name = name
        self.caves = []
        self.visit_count = 0

    def connect(self, c):
        self.caves.append(c)

    def __repr__(self):
        return f"<{self.name}>"


all_caves = {}


for line in input:
    c1, c2 = line.strip().split("-")

    if c1 not in all_caves:
        cave1 = Cave(c1)
        all_caves[c1] = cave1
    else:
        cave1 = all_caves[c1]
    if c2 not in all_caves:
        cave2 = Cave(c2)
        all_caves[c2] = cave2
    else:
        cave2 = all_caves[c2]

    cave1.connect(cave2)
    cave2.connect(cave1)


def search(cave, paths, cur_path, part):

    cur_path = tuple(list(cur_path) + [cave.name])
    if cave.name == "end":
        paths.add(cur_path)
        return

    if part == 1:
        if cave.visit_count > 1 and cave.tp == "small":
            return
    elif part == 2:
        ct = 0

        freqs = {}
        for c in cur_path:
            if c.lower() == c:
                freqs[c] = freqs.get(c, 0) + 1

        for k, v in freqs.items():
            if v > 2:
                return
            if v == 2:
                ct += 1

        if ct > 1:
            return

    for c in cave.caves:
        if c.name == "start":
            # ignore
            continue
        c.visit_count += 1
        search(c, paths, cur_path, part)
        c.visit_count -= 1


paths = set()
search(all_caves["start"], paths, tuple(), 1)
print("part1", len(paths))


paths = set()
search(all_caves["start"], paths, tuple(), 2)
print("part2", len(paths))
