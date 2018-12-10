import re
from get_data import get_data_lines

data = get_data_lines(10)

def find_numbers(string, ints=True):
    numexp = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*') #optional - in front
    numbers = numexp.findall(string)
    numbers = [x.replace(',','') for x in numbers]
    if ints is True:
        return [int(x.replace(',','').split('.')[0]) for x in numbers]
    else:
        return numbers


new_data = []
for line in data:
    new_data.append(find_numbers(line, True))

GRID_SIZE = 600


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


points = []

for pt in new_data:
    points.append(Point(pt[0], pt[1], pt[2], pt[3]))

print(points)


def gen_image(points, t):
    grid = []
    for x in range(GRID_SIZE):
        grid.append([0] * GRID_SIZE)

    for pt in points:
        grid[int(pt.y+GRID_SIZE/2)][int(pt.x+GRID_SIZE/2)] = 1

    with open(f'./images/{t}.pbm', 'w') as f:
        f.write('P1\n')
        f.write(f'{GRID_SIZE} {GRID_SIZE}\n')

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                f.write(f'{grid[row][col]} ')
            f.write('\n')


for t in range(12000):
    in_range = True
    for idx, pt in enumerate(points):

        pt.x += pt.vx
        pt.y += pt.vy

    for pt in points:
        if not(pt.x > -GRID_SIZE/2 and pt.x < GRID_SIZE/2 and pt.y >-GRID_SIZE/2 and pt.y < GRID_SIZE/2):
            in_range = False
            break

    if in_range:
        print('in range at time', t)

        gen_image(points, t)
