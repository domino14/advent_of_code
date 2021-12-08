input = open("/Users/cesar/08/input.txt", "r").readlines()

# input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf".split(
#     "\n"
# )

nums = 0
for line in input:
    line = line.strip()
    line = line.split(" | ")
    for x in line[1].split():
        if len(x) == 7 or len(x) == 2 or len(x) == 3 or len(x) == 4:
            nums += 1

print("p1", nums)


# Part 2


def solve(line):

    # find top segment:
    for pat in line.split():
        if len(pat) == 2:
            pat2 = set(list(pat))
        if len(pat) == 3:
            pat3 = set(list(pat))
        if len(pat) == 4:
            pat4 = set(list(pat))

    t = list(pat3 - pat2)[0]

    # find tl and m
    tlm = list(pat4 - pat2)

    ct_0 = 0
    ct_1 = 0
    for pat in line.split():
        if tlm[0] in pat:
            ct_0 += 1
        if tlm[1] in pat:
            ct_1 += 1

    if ct_0 == 7:
        assert ct_1 == 6
        # this is the middle segment
        m = tlm[0]
        tl = tlm[1]
    elif ct_1 == 7:
        assert ct_0 == 6
        # this is the middle segment
        m = tlm[1]
        tl = tlm[0]

    # find bottom right segment
    cts = {}
    for pat in line.split():
        for c in list(pat):
            if c in cts:
                cts[c] += 1
            else:
                cts[c] = 1
    for k, v in cts.items():
        if v == 4:
            bl = k
        if v == 9:
            br = k

    tr = list(pat2 - set(br))[0]

    # we have t, tl, m, br, tr, bl

    # find bottom segment by process of elinination
    b = set(["a", "b", "c", "d", "e", "f", "g"]) - set([m, tl, bl, br, t, tr])
    b = list(b)[0]

    return {tl: "b", m: "d", tr: "c", bl: "e", b: "g", br: "f", t: "a"}


nums = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


sum = 0
for line in input:
    line = line.strip()
    line = line.split(" | ")

    m = solve(line[0])

    outputs = line[1].split()

    num = ""

    for x in outputs:
        s = ""
        for c in x:
            s += m[c]

        num += str(nums["".join(sorted(list(s)))])
    sum += int(num)

print(sum)
