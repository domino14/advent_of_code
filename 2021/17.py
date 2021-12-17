xmin, xmax = (230, 283)
ymin, ymax = (-107, -57)

start = (0, 0)


def launch(xv, yv, start, xmin, xmax, ymin, ymax):
    pos = start
    maxy = -1000000000

    while pos[0] < xmax + 10 and pos[1] >= ymin:
        # step
        px = pos[0] + xv
        py = pos[1] + yv

        if xv > 0:
            xv -= 1
        elif xv < 0:
            xv += 1

        yv -= 1
        if py > maxy:
            maxy = py
        pos = (px, py)

        if pos[0] >= xmin and pos[0] <= xmax and pos[1] >= ymin and pos[1] <= ymax:
            # made it
            return maxy



maxy = -100000000
vals = 0
for xv in range (0, 580):
    for yv in range (-500, 1000):
        topy = launch(xv, yv, start, xmin, xmax, ymin, ymax)
        if topy is not None:
            vals += 1
            if topy > maxy:
                maxy = topy


print('p1', maxy)
print('p2', vals)

