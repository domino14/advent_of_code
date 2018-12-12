sn = 18

pl_cache = {}


def pl(x, y, sn):
    """
    >>> pl(3, 5, 8)
    4

    >>> pl(122, 79, 57)
    -5

    >>> pl(217, 196, 39)
    0

    >>> pl(101, 153, 71)
    4

    """
    if (x, y) in pl_cache:
        return pl_cache[(x, y)]

    rack_id = x + 10
    power_level = rack_id * y
    power_level += sn
    power_level *= rack_id
    power_level = int(power_level/100)
    power_level = int(str(power_level)[-1])
    power_level -= 5
    pl_cache[(x, y)] = power_level

    return power_level


def sq_power(tlx, tly, size):
    tpl = 0
    for x in range(tlx, tlx+size):
        for y in range(tly, tly+size):
            tpl += pl(x, y, sn)    
    return tpl


if __name__ == '__main__':
    BIGGEST_SIZE = 20
    max_pl = 0
    max_xy = (0, 0)
    max_size = 0
    for x in range(1, 299):
        for y in range(1, 299):
            for size in range(1, min(BIGGEST_SIZE+1-x, BIGGEST_SIZE+1-y)):

                tpl = sq_power(x, y, size)
                if tpl > max_pl:
                    max_pl = tpl
                    max_xy = (x, y)
                    max_size = size

    print(max_pl)
    print(max_xy)
    print(max_size)
