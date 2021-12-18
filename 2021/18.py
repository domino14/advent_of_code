input = open("./18/input.txt", "r").readlines()


def find_explodes(s: list, depth: int, coord: tuple, nested_pairs: list):
    s1 = None
    s2 = None
    try:
        s1 = s[0]
    except TypeError:
        # s is a lone number
        pass

    try:
        s2 = s[1]
    except TypeError:
        pass

    if (
        type(s) == list
        and type(s[0]) == int
        and type(s[1]) == int
        and depth >= 4
    ):
        nested_pairs.append(coord)

    if s1 is not None:
        find_explodes(s1, depth + 1, tuple(list(coord) + [0]), nested_pairs)
    if s2 is not None:
        find_explodes(s2, depth + 1, tuple(list(coord) + [1]), nested_pairs)


def find_splits(s: list, coord: tuple, coords: list):
    s1 = None
    s2 = None
    try:
        s1 = s[0]
    except TypeError:
        # s is a lone number
        pass

    try:
        s2 = s[1]
    except TypeError:
        pass

    if s1 is not None:
        find_splits(s1, tuple(list(coord) + [0]), coords)
    if s2 is not None:
        find_splits(s2, tuple(list(coord) + [1]), coords)
    if type(s) == int and s >= 10:
        coords.append(coord)


def binaryadd(t: tuple, a: int):
    b = "".join(map(lambda y: str(y), t))
    val = int(b, 2)
    newb = format(val + a, "b")
    if len(newb) < len(b):
        newb = "0" * (len(b) - len(newb)) + newb
    return tuple(map(lambda y: int(y), newb))


def val_at_coord(s: list, c: tuple):
    l = s
    for cc in c:
        l = l[cc]

    return l


def set_at_coord(s: list, c: tuple, toset):
    # this is HORRIBLE, but python has no pointers
    if len(c) == 1:
        s[c[0]] = toset
    elif len(c) == 2:
        s[c[0]][c[1]] = toset
    elif len(c) == 3:
        s[c[0]][c[1]][c[2]] = toset
    elif len(c) == 4:
        s[c[0]][c[1]][c[2]][c[3]] = toset
    elif len(c) == 5:
        s[c[0]][c[1]][c[2]][c[3]][c[4]] = toset
    else:
        raise Exception(f"set_at_coord failed, s={s}, c={c}, toset={toset}")


def reduce(s: list):
    # explode then split
    # find leftmost pair to explode

    processing = True

    while processing:
        exploding = True
        while exploding:
            pairs = []
            find_explodes(s, 0, tuple(), pairs)
            if len(pairs) == 0:
                exploding = False
            if len(pairs) > 0:
                to_explode = pairs[0]
                int1 = None
                int2 = None
                b = "".join(map(lambda y: str(y), to_explode))

                news = s
                # look left
                intcoord1 = []
                intcoord2 = []
                if not all([x == 0 for x in to_explode]):
                    left = binaryadd(to_explode, -1)
                    for v in left:
                        news = news[v]
                        intcoord1.append(v)
                        if type(news) == int:
                            int1 = news
                            break

                    # if news is still a list, keep going down
                    if type(news) == list:
                        while type(news) == list:
                            news = news[1]
                            intcoord1.append(1)
                        int1 = news

                # otherwise they're all 0s, so there's nothing to the left.
                # look right
                news = s
                right = binaryadd(to_explode, 1)
                if len(right) == len(to_explode):
                    for v in right:
                        news = news[v]
                        intcoord2.append(v)
                        if type(news) == int:
                            int2 = news
                            break

                    if type(news) == list:
                        while type(news) == list:
                            news = news[0]
                            intcoord2.append(0)
                        int2 = news

                # otherwise, it's all 1s, so there's nothing to the right.
                explodevals = val_at_coord(s, to_explode)
                if int1 is not None:
                    set_at_coord(s, intcoord1, int1 + explodevals[0])

                if int2 is not None:
                    set_at_coord(s, intcoord2, int2 + explodevals[1])

                set_at_coord(s, to_explode, 0)

        # try splitting
        coords = []
        find_splits(s, tuple(), coords)
        if len(coords) == 0:
            processing = False
        else:
            to_split = coords[0]
            val = val_at_coord(s, to_split)
            l = val // 2
            r = val - l
            set_at_coord(s, to_split, [l, r])

    return s


def add(i: list, j: list):
    sum = [i, j]
    return reduce(sum)


def magnitude(s):
    if type(s) == list:
        return 3 * magnitude(s[0]) + 2 * magnitude(s[1])
    return s


last = eval(input[0].strip())
for l in input[1:]:
    last = add(last, eval(l.strip()))


print("p1: ", magnitude(last))


max_mag = -1

for i in range(len(input)):
    if i % 10 == 0:
        print("trying", i)
    for j in range(len(input)):
        max_mag = max(
            magnitude(add(eval(input[i].strip()), eval(input[j].strip()))),
            max_mag,
        )


print("p2: ", max_mag)
