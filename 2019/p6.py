from get_data import get_data_lines

lines = get_data_lines(6)

# print(lines)


# child orbits around parent
class Planet:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.visited = False

    def set_visited(self, visitor, depth=None):
        # print(f"I am {self.name}, visitor came from {visitor} (Depth {depth})")
        self.visited = True

    def add_child(self, child):
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def __repr__(self):
        return (
            f"<Planet {self.name}, "
            f"children {list(map( lambda n: n.name, self.children))} "
            f"parent {self.parent.name if self.parent else 'nil'}>"
        )


planets = {}

# lines = [
#     "COM)B",
#     "B)C",
#     "C)D",
#     "D)E",
#     "E)F",
#     "B)G",
#     "G)H",
#     "D)I",
#     "E)J",
#     "J)K",
#     "K)L",
#     "K)YOU",
#     "I)SAN",
# ]

for i in lines:
    par, ch = i.split(")")

    if par not in planets:
        parent_planet = Planet(par)
        planets[par] = parent_planet
    else:
        parent_planet = planets[par]

    if ch not in planets:
        child_planet = Planet(ch)
        planets[ch] = child_planet
    else:
        child_planet = planets[ch]
    parent_planet.add_child(child_planet)
    child_planet.set_parent(parent_planet)


# print(planets)
count = 0

for k, p in planets.items():
    par = p.parent
    while par:
        count += 1
        par = par.parent

print(count)

# part 2

you = planets["YOU"]
san = planets["SAN"]
san_parent = san.parent

depth = 0
print(planets["COM"])


def find_insertion(depth, currently_orbiting):
    # found when we orbit same object san is orbiting
    if currently_orbiting.parent is None:
        return

    if currently_orbiting.parent.name == san_parent.name:
        print(depth - 1)
        return

    currently_orbiting.set_visited(None, depth)

    if (
        not currently_orbiting.parent.visited
        and currently_orbiting.parent.name != "YOU"
    ):
        find_insertion(depth + 1, currently_orbiting.parent)
        # currently_orbiting.parent.set_visited(currently_orbiting, depth)

    for c in currently_orbiting.children:
        if not c.visited and c.name != "YOU":
            # c.set_visited(currently_orbiting, depth)
            find_insertion(depth + 1, c)


find_insertion(depth, you.parent)
