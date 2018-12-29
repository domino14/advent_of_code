import random
import re

from get_data import get_data_lines


data = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".split('\n')
data = get_data_lines(23)

coords = []

random.seed()

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
    print(f'Bounding box: {bb}')
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bb
    print(f'Number of iterations: '
          f'{(xmax - xmin) * (ymax - ymin) * (zmax - zmin) * len(coords)}')
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
        print(f'{x}...')
    print(mdist(maxcoord, (0, 0, 0)))


def part2_mc(coords, bb=None, iters=500, tries_per_iter=10000):
    # Try a Monte Carlo solution??
    if not bb:
        bb = boundingbox(coords)
    print(f'Bounding box: {bb}')
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = bb

    maxmax = -1
    maxmaxcoord = None
    for iter in range(iters):

        maxinrange = -1
        maxcoord = None
        for i in range(tries_per_iter):
            x = random.randint(xmin, xmax)
            y = random.randint(ymin, ymax)
            z = random.randint(zmin, zmax)

            inrange = 0
            for nanobot in coords:
                if mdist(nanobot, (x, y, z)) <= nanobot[3]:
                    inrange += 1

            if inrange > maxinrange:
                maxinrange = inrange
                maxcoord = (x, y, z)

        if maxinrange > maxmax:
            maxmax = maxinrange
            maxmaxcoord = maxcoord

            print(iter, maxmax, maxmaxcoord, mdist(maxmaxcoord, (0, 0, 0)))


def part2_mc_redux(coords):
    # got from part2_mc
    # 841 (36568201, 28672935, 53966997) 119208133
    # 844 (36576730, 30094990, 56562275) 123233995
    # 871 (36362489, 31154379, 53633672) 121150540
    # 875 (35147893, 32005985, 53975165) 121129043
    # 876 (33265838, 33160886, 53065151) 119491875

    # 880 (34352335, 33155035, 53240644) 120748014
    # 881 (35052813, 29331280, 54627237) 119011330
    # 888 (34540220, 30205520, 54265592) 119011332

    bb = ((34352335, 35052813), (29331280, 33155035), (53240644, 54627237))
    part2_mc(coords, bb, 500, 1000)


def part2_binary_search(coords):
    guess = (34613362, 30639463, 53758517)

    for exp in range(24, 0, -1):
        maxinrange = -1
        maxcoord = None
        dist = 2 ** exp
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    inrange = 0
                    coords_to_check = (x * dist + guess[0],
                                       y * dist + guess[1],
                                       z * dist + guess[2])
                    for nanobot in coords:
                        if mdist(nanobot, coords_to_check) <= nanobot[3]:
                            inrange += 1

                    if inrange > maxinrange:
                        maxinrange = inrange
                        maxcoord = coords_to_check
                        guess = coords_to_check

        print(maxinrange, maxcoord, mdist(maxcoord, (0, 0, 0)))


if __name__ == '__main__':
    part2_binary_search(coords)

