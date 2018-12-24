r5 = 1
r4 = 1
r1 = 943  # 10551343 for the giant case
r0 = 1

# r1 = 35  # 1 + (5  + 7 + 35 + 1) =
r1 = 949   # 1 + (1 + 13 + 73 + 949) = 1037
r1 = 1515  # 1 + (1 + 3 + 5 + 101 + 1515) = 1626
r1 = 10551343

if False:
    # Inefficient factorizer
    while True:
        # print(f'r0={r0} r1={r1} r4={r4} r5={r5}')
        if r5 * r4 == r1:
            print(f'{r5} * {r4} == {r1}, adding {r5} to r0, r0 now = {r0}')
            r0 += r5   # add r5 factor
        r4 += 1
        if r4 > r1:
            r5 += 1
            r4 = 1
        if r5 > r1:
            break

    print('at the end', r0)

else:
    s = 0
    for i in range(1, r1 + 1):
        if r1 % i == 0:
            print(f'{i} is a factor')
            s += i

    print('at the end', s)
