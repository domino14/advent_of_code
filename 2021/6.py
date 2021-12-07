import math

input = open("/Users/cesar/06/input.txt", "r").readlines()

# input = "3,4,3,1,2".split("\n")

numbers = [int(n) for n in input[0].split(",")]


class LF:
    timer = 0

    def __init__(self, timer):
        self.timer = timer

    def __repr__(self):
        return f"{self.timer}"


repr_every = 7
born_delay = 2


def fishies(days):

    fishes = [LF(n) for n in numbers]
    day = 0
    while day < days:
        new_fishes = []
        for f in fishes:
            # if f.new:
            # f.timer -= 1
            f.timer -= 1
            if f.timer == -1:
                nf = LF(repr_every + born_delay - 1)
                f.timer = repr_every - 1
                new_fishes.append(nf)

        fishes.extend(new_fishes)
        day += 1
        # print(fishes)
    return len(fishes)


print(fishies(80))

## part 2

# see 6.go for ridiculous brute-force solution of the 1-case
fishes_after = {
    1: 6206821033,  # after 256 days
    2: 5617089148,  # 255 days
    3: 5217223242,  # and so forth
    4: 4726100874,
    5: 4368232009,
}
sum = 0
for n in numbers:
    sum += fishes_after[n]

print(sum)