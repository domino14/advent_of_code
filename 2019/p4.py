from get_data import get_data_lines, find_numbers


l = 248345
h = 746315

crit = 0


def matches(n):
    lastd = ""
    baddig = False
    match = False
    for d in str(n):
        if d == lastd:
            match = True

        # print("check", lastd, int(d))
        if lastd != "" and int(d) < int(lastd):
            # print("oops", d, lastd)
            baddig = True

        lastd = d
    # print("match", match)
    # print("baddig", baddig)

    if match and not baddig:
        return True

    return False


def matchesp2(n):
    lastd = ""
    baddig = False
    match = False
    groups = []

    for d in str(n):
        if d == lastd:
            # if match:
            #     match = False
            #     repeatdig = d
            # else:
            #     if d != repeatdig:
            #         match = True
            groups[-1] = groups[-1] + d
        else:
            groups.append(d)

        if lastd != "" and int(d) < int(lastd):
            # print("oops", d, lastd)
            baddig = True

        lastd = d
    # print("match", match)
    # print("baddig", baddig)
    # print(groups)
    if any([len(g) == 2 for g in groups]):
        match = True

    if match and not baddig:
        return True

    return False


if __name__ == "__main__":
    for i in range(l, h + 1):
        if matches(i):
            crit += 1

    print("p1", crit)
    crit = 0
    for i in range(l, h + 1):
        if matchesp2(i):
            crit += 1

    print("p2", crit)

