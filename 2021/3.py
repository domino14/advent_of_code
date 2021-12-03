input = open("/Users/cesar/03/input.txt", "r").readlines()
ll = len(input[0].strip())


def zo_calc(input_lines):
    zeros = {}
    ones = {}

    for line in input_lines:
        line = line.strip()
        for idx, c in enumerate(line):
            if c == "0":
                if idx in zeros:
                    zeros[idx] += 1
                else:
                    zeros[idx] = 1
            if c == "1":
                if idx in ones:
                    ones[idx] += 1
                else:
                    ones[idx] = 1

    return zeros, ones


zeros, ones = zo_calc(input)


gam = list("0" * ll)
eps = list("0" * ll)

for k, v in zeros.items():
    if v > ones[k]:
        gam[k] = "0"
        eps[k] = "1"
    else:
        gam[k] = "1"
        eps[k] = "0"

gr = int("".join(gam), 2)
er = int("".join(eps), 2)

print("1:", gr * er)

## part two


def life_support(typ):
    keep = set(input)

    for k in range(len(gam)):
        new_keep = set()

        zeros, ones = zo_calc(list(keep))

        if (typ == "ox" and ones[k] >= zeros[k]) or (
            typ == "co2" and ones[k] < zeros[k]
        ):
            for item in keep:
                if item[k] == "1":
                    new_keep.add(item)

            keep = new_keep
        else:
            for item in keep:
                if item[k] == "0":
                    new_keep.add(item)
            keep = new_keep

        if len(keep) == 1:
            return int(keep.pop(), 2)


print("2:", life_support("ox") * life_support("co2"))
