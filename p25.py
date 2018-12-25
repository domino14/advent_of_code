from get_data import get_data_lines

lines = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""".split('\n')

lines = get_data_lines(25)

def mdist(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]) + (
        abs(c1[3] - c2[3]))


coords = []
for coord in lines:
    coords.append(tuple([int(i) for i in coord.split(',')]))


constellations = []


class Constellation:
    def __init__(self):
        self.pts = set()
        self.active = True

    def __repr__(self):
        return f'{self.pts}'

    def can_join(self, other_c):
        for mypt in self.pts:
            for otherpt in other_c.pts:
                if mdist(mypt, otherpt) <= 3:
                    return True
        return False

    def append(self, pt):
        self.pts.add(pt)


def in_constellation(coord, constellation):
    for pt in constellation.pts:
        if mdist(coord, pt) <= 3:
            return True
    return False


for coord in coords:
    # create a constellation if not exist
    joined = False
    # find a constellation to join
    for constellation in constellations:
        if in_constellation(coord, constellation):
            constellation.append(coord)
            joined = True
            break
    if not joined:
        # Create a new constellation
        c = Constellation()
        c.append(coord)
        constellations.append(c)


print(constellations)


while True:
    merged = False
    for c1 in constellations:
        for c2 in constellations:
            if c1 != c2 and c1.can_join(c2):
                c1.active = False
                c2.pts.update(c1.pts)
                c1.pts = set()
                merged = True
    if merged is False:
        break


print(len(list(filter(lambda c: c.active, constellations))))



