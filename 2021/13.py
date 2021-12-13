input = open("./13/input.txt", "r").readlines()


dots = set()
inst = []
parse_dots = True
for line in input:
    if line.strip() == "":
        parse_dots = False
        continue
    if parse_dots:
        x, y = line.strip().split(",")
        dots.add((int(x), int(y)))
    else:
        a, b = line.split("fold along ")
        axis, n = b.split("=")
        inst.append((axis, int(n)))


def fold(axis, n, dots, new_dots):
    for dot in dots:
        check = dot[1] if axis == "y" else dot[0]
        if check > n:
            if axis == "y":
                new_dot = (dot[0], (2 * n) - check)
            else:
                new_dot = ((2 * n) - check, dot[1])
        else:
            new_dot = dot
        new_dots.add(new_dot)


new_dots = set()


for i in range(len(inst)):
    fold(inst[i][0], inst[i][1], dots, new_dots)
    if i == 0:
        print("part 1: ", len(new_dots))
    dots = new_dots
    new_dots = set()


maxr = max([x[0] for x in dots])
maxc = max([x[1] for x in dots])
st = ""

for r in range(0, maxc + 1):
    for c in range(0, maxr + 1):
        st += "# " if (c, r) in dots else ". "
    st += "\n"
print(st)
