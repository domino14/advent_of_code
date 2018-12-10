from get_data import get_data_lines

data = get_data_lines(10)

data = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".split('\n')


import re

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

    def __repr__(self):
        return f'<{self.x}, {self.y}> v=<{self.vx}, {self.vy}>'
    
points = []
    
for pt in new_data:
    points.append(Point(pt[0], pt[1], pt[2], pt[3]))

print(points)


def gen_image(points, t):
    # make grid
#    for 
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
