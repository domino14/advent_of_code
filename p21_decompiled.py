
r0 = 12454098   # I control this.

r1 = 0

loops = 0

part1 = False
last_r1 = None


def inner_fn():
    global r5, r1, loops, part1, last_r1

    while True:
        loops += 1
        r1 = r1 + (r5 & 255)
        r1 = ((r1 & 16777215) * 65899) & 16777215
        if r5 < 256:
            # THE STOPPING CONDITION
            # if r1 == r0:
            #     return False
            # else:
            #     return True

            if not part1:
                print(f'Part 1: {r1}')
                part1 = True
            # return False
            if r1 == 5970144 and last_r1 is not None:  # part 1 answer
                print(f'Part 2: {last_r1}, cycle={r1}')
                return False
                # 1974943 is too low apparently.
            last_r1 = r1
        else:
            r5 = int(r5 / 256)


while True:
    r5 = r1 | (1 << 16)
    r1 = 8586263

    ret = inner_fn()
    if not ret:
        break



