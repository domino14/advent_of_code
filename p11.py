sn = 3628

sq_pw_cache = {}


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
    # if (x, y) in pl_cache:
    #     return pl_cache[(x, y)]

    rack_id = x + 10
    power_level = rack_id * y
    power_level += sn
    power_level *= rack_id
    power_level = int(power_level/100) % 10 - 5
    # pl_cache[(x, y)] = power_level

    return power_level


def sq_power(tlx, tly, size):
    if (tlx, tly, size) in sq_pw_cache:
        return sq_pw_cache[(tlx, tly, size)]
    if size == 1:
        c = pl(tlx, tly, sn)
        sq_pw_cache[(tlx, tly, size)] = c
        return c
    tpl = 0

    x = tlx + size - 1
    for y in range(tly, tly + size):
        tpl += pl(x, y, sn)
    y = tly + size - 1
    for x in range(tlx, tlx + size - 1):
        tpl += pl(x, y, sn)

    tpl += sq_power(tlx, tly, size-1)
    sq_pw_cache[(tlx, tly, size)] = tpl
    return tpl



if __name__ == '__main__':
    max_pl = 0
    max_xy = (0, 0)
    max_size = 0
    for x in range(1, 301):
        for y in range(x, 301):
            for size in range(x, 301):
                tpl = sq_power(x, y, size)
                if tpl > max_pl:
                    max_pl = tpl
                    max_xy = (x, y)
                    max_size = size
        print(f'{x}...')

    print(f'Max power: {max_pl}')
    print(max_xy)
    print(max_size)

