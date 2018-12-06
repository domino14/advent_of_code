with open('./input/3.txt') as f:
    claims = f.read()


def parse_claim(claim):
    cid, atsign, coords, area = claim.split(' ')
    coords = coords[:-1]
    cx, cy = coords.split(',')
    dx, dy = area.split('x')
    return int(cx), int(cy), int(dx), int(dy), int(cid[1:])


claims = claims.split('\n')

limit = 1100
patchwork = []
for i in range(limit):
    # each of this is a row
    patchwork.append(list('.' * limit))

overlaps = {}

for claim in claims:
    parsed = parse_claim(claim)
    for x in range(parsed[0], parsed[0] + parsed[2]):
        for y in range(parsed[1], parsed[1] + parsed[3]):
            if patchwork[x][y] == '.':
                patchwork[x][y] = [parsed[4]]
            elif type(patchwork[x][y]) == list:
                overlaps[parsed[4]] = True
                overlaps[patchwork[x][y][0]] = True
                patchwork[x][y].append(parsed[4])


n_overlaps = 0
for x in range(limit):
    for y in range(limit):
        if type(patchwork[x][y]) == list and len(patchwork[x][y]) > 1:
            n_overlaps += 1

print(f'part 1: {n_overlaps}')

for claim in claims:
    parsed = parse_claim(claim)
    if parsed[4] not in overlaps:
        print(f'part 2: {parsed[4]}')
