from get_data import get_data_lines, find_numbers


# model as intersections of many line segments
def find_intersection(p0, p1, p2, p3):

    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0:
        return None  # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive:
        return None  # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive:
        return None  # no collision

    if (s_numer > denom) == denom_is_positive or (
        t_numer > denom
    ) == denom_is_positive:
        return None  # no collision

    # collision detected

    t = t_numer / denom

    intersection_point = [
        round(p0[0] + (t * s10_x)),
        round(p0[1] + (t * s10_y)),
    ]

    return intersection_point


inp = get_data_lines(3)
# inp = [
#     "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
#     "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
# ]
# inp = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
# inp = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]


wire1 = inp[0].split(",")
wire2 = inp[1].split(",")


def line_segments(wire_inst):
    x0 = 0
    y0 = 0
    segs = []
    for inst in wire_inst:
        n = find_numbers(inst)[0]
        dir = inst[0]
        if dir == "R":
            x1 = x0 + n
            y1 = y0
        if dir == "L":
            x1 = x0 - n
            y1 = y0
        if dir == "U":
            x1 = x0
            y1 = y0 + n
        if dir == "D":
            x1 = x0
            y1 = y0 - n
        segs.append([(x0, y0), (x1, y1)])
        x0, y0 = x1, y1
    return segs


ls1 = line_segments(wire1)
ls2 = line_segments(wire2)


def mdist(p0, p1):
    return abs(p1[1] - p0[1]) + abs(p1[0] - p0[0])


centerloc = (0, 0)
mindist = 100000000

intersection_pts = []
for seg1 in ls1:
    for seg2 in ls2:
        pt = find_intersection(seg1[0], seg1[1], seg2[0], seg2[1])
        if pt and pt != [0, 0]:
            d = mdist(centerloc, pt)
            if d < mindist:
                mindist = d
            intersection_pts.append(pt)

print(mindist)


def wire_traverse_dist(wire_inst, pt):
    """ distance that we travel along wire to reach pt """
    # this function is super ghetto
    x0 = 0
    y0 = 0
    x, y = pt
    dist_traveled = 0
    for inst in wire_inst:
        n = find_numbers(inst)[0]
        dir = inst[0]
        if dir == "R":
            x1 = x0 + n
            y1 = y0
        if dir == "L":
            x1 = x0 - n
            y1 = y0
        if dir == "U":
            x1 = x0
            y1 = y0 + n
        if dir == "D":
            x1 = x0
            y1 = y0 - n

        # we are always traveling from x0, y0 to x1, y1
        if x1 == x0 and x == x0:
            if y > min(y0, y1) and y < max(y0, y1):
                dist_traveled += abs(y - y0)
                return dist_traveled

        elif y1 == y0 and y == y0:
            if x > min(x0, x1) and x < max(x0, x1):
                dist_traveled += abs(x - x0)
                return dist_traveled

        else:
            # print("Adding to dist traveled, lenght of wire", n)
            dist_traveled += n

        x0, y0 = x1, y1

    raise Exception("did not intersect after all?", wire_inst, pt)


# part2
minsum = 100000000
print("intersection pts", intersection_pts)
for pt in intersection_pts:
    print("checking", pt)
    d1 = wire_traverse_dist(wire1, pt)
    print("and wire2")
    d2 = wire_traverse_dist(wire2, pt)
    if d1 + d2 < minsum:
        minsum = d1 + d2

print(minsum)

