input = open("/Users/cesar/07/input.txt", "r").readlines()


nums = [int(n) for n in input[0].split(",")]
# nums = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

large_n = 1e10


def align(p1=False):
    min_pos = min(nums)
    max_pos = max(nums)

    min_fuel = large_n

    for x in range(min_pos, max_pos + 1):
        fuel = 0
        for idx, pos in enumerate(nums):
            # Try moving all of them to x
            if p1:
                fuel += abs(pos - x)
            else:
                fuel += (abs(pos - x) * (abs(pos - x) + 1)) // 2

        if fuel < min_fuel:
            min_fuel = fuel

    print(min_fuel)


align(True)
align(False)