import re

from get_data import get_data_lines


data = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".split('\n')
# data = get_data_lines(23)

coords = []


def mdist(c1, c2):
    # print (f'dist between {c1} and {c2}')
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])


def nums(mystr):
    return [int(i) for i in re.findall(r'(-?\d+)', mystr)]


for up in data:
    coords.append(nums(up))


def part1(coords):

    strongest = max([(c[3], idx) for idx, c in enumerate(coords)])
    strongest_pt = coords[strongest[1]]  # Look up by idx

    inrange = 0
    for c in coords:
        if mdist(c, strongest_pt) <= strongest_pt[3]:
            inrange += 1

    print(inrange)


def boundingbox(coords):
    """ return (x, y, z) where x, y, z are 2-tuples (min, max) """
    xmin, xmax = min([c[0] for c in coords]), max([c[0] for c in coords])
    ymin, ymax = min([c[1] for c in coords]), max([c[1] for c in coords])
    zmin, zmax = min([c[2] for c in coords]), max([c[2] for c in coords])

    return ((xmin, xmax), (ymin, ymax), (zmin, zmax))


def part2(coords):
    # this is the naive solution 😩
    # figure out the bounding box
    bb = boundingbox(coords)
    print(bb)
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bb
    maxinrange = -1
    maxcoord = None
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            for z in range(zmin, zmax + 1):
                inrange = 0
                for nanobot in coords:
                    if mdist(nanobot, (x, y, z)) <= nanobot[3]:
                        inrange += 1

                if inrange > maxinrange or (
                    inrange == maxinrange and
                        mdist((x, y, z), (0, 0, 0)) < mdist(maxcoord, (0, 0, 0))):

                    maxinrange = inrange
                    maxcoord = (x, y, z)

    print(mdist(maxcoord, (0, 0, 0)))


if __name__ == '__main__':
    part2(coords)


