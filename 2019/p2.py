import requests

from get_data import get_data_lines, get_data, find_numbers

inp = get_data(2)

opcodes = inp.split(",")
print(opcodes)
insts = []
for i in range(0, len(opcodes), 4):
    inst = opcodes[i : i + 4]
    insts.append(inst)

print(insts)


opcodes[1] = 12
opcodes[2] = 2

# opcodes = [1, 1, 1, 4, 99, 5, 6, 0, 99]


def run_prog(opcodes):
    # part 1
    prog_ptr = 0

    while True:
        to_exec = int(opcodes[prog_ptr])
        if to_exec == 1:
            # sum
            s1, s2 = int(opcodes[prog_ptr + 1]), int(opcodes[prog_ptr + 2])
            res = int(opcodes[prog_ptr + 3])
            opcodes[res] = int(opcodes[s1]) + int(opcodes[s2])
        elif to_exec == 2:
            s1, s2 = int(opcodes[prog_ptr + 1]), int(opcodes[prog_ptr + 2])
            res = int(opcodes[prog_ptr + 3])
            opcodes[res] = int(opcodes[s1]) * int(opcodes[s2])
        elif to_exec == 99:
            # print("found 99, halting")
            break
        else:
            print("unexpected opcode " + str(to_exec))
            break
        prog_ptr += 4
    return opcodes[0]


print(run_prog(opcodes))

# part 2
for a in range(0, 100):
    for b in range(0, 100):
        opcodes = inp.split(",")
        opcodes[1] = a
        opcodes[2] = b
        ret = run_prog(opcodes)
        if ret == 19690720:
            print(a, b, "wanted:", 100 * a + b)
            break
