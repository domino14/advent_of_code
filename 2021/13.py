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
        if axis == "y":
            # fold up
            if dot[1] > n:
                new_y = (2 * n) - dot[1]
                new_dots.add((dot[0], new_y))
            else:
                new_dots.add(dot)
        if axis == "x":
            if dot[0] > n:
                # fold left
                new_x = (2 * n) - dot[0]
                new_dots.add((new_x, dot[1]))

            else:
                new_dots.add(dot)


new_dots = set()


for i in range(len(inst)):
    fold(inst[i][0], inst[i][1], dots, new_dots)
    if i == 0:
        print("part 1: ", len(new_dots))
    dots = new_dots
    new_dots = set()

mat = [["." for x in range(40)] for y in range(40)]
for dot in dots:
    mat[dot[0]][dot[1]] = "#"

minr = min([x[0] for x in dots])
maxr = max([x[0] for x in dots])
minc = min([x[1] for x in dots])
maxc = max([x[1] for x in dots])
st = ""

for r in range(minc, maxc + 1):
    for c in range(minr, maxr + 1):
        st += mat[c][r] + " "
    st += "\n"
print(st)
