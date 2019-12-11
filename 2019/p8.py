from get_data import get_data

inp  = get_data(8).strip()

width = 25
height = 6

# inp = '0222112222120000'
# width = 2
# height = 2

num_layers = len(inp) / (width * height)
print(len(inp))
print(num_layers)
idx = -1
fewest_zeros = 100000000
for l in range(int(num_layers)):
    num_zeros = 0
    num_ones = 0
    num_twos = 0
    for x in range(width):
        for y in range(height):
            idx += 1
            dig = inp[idx]
            if dig == '0':
                num_zeros += 1
            if dig == '1':
                num_ones += 1
            if dig == '2':
                num_twos += 1
    if num_zeros < fewest_zeros:
        fewest_zeros = num_zeros
        fewest_mult = num_ones * num_twos

print (fewest_mult)

# part 2 - 3d array
arr = []
idx = -1
for l in range(int(num_layers)):
    arr.append([])
    for y in range(height):
        arr[l].append([])
        for x in range(width):
            idx += 1
            dig = inp[idx]
            arr[l][y].append(dig)

disp_arr = []
for y in range(height):
    disp_arr.append([])
    for x in range(width):
        for l in range(int(num_layers)):
            if arr[l][y][x] == '2':
                # continue, transparent
                continue
            else:
                disp_arr[y].append(arr[l][y][x])
                break

for y in range(height):
    str = ""
    for x in range(width):
        if disp_arr[y][x] == '1':
            str += '.'
        else:
            str += ' '
    print(str)