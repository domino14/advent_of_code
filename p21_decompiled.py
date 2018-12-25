r1 = 0

part1 = False
last_r1 = None

seen_numbers = set()


def inner_fn():
    global r5, r1, part1, last_r1, seen_numbers

    while True:
        r1 = r1 + (r5 & 255)
        r1 = ((r1 & 16777215) * 65899) & 16777215
        if r5 < 256:

            if not part1:
                print(f'Part 1: {r1}')
                part1 = True
            if r1 not in seen_numbers:
                seen_numbers.add(r1)
                last_r1 = r1
                return True
            else:
                print(f'Part 2: {last_r1}')
                # 1974943 is WRONG!
                return False

        else:
            r5 = int(r5 / 256)


while True:
    r5 = r1 | (1 << 16)
    r1 = 8586263

    ret = inner_fn()
    if not ret:
        break

