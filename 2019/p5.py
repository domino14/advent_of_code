from get_data import get_data_lines, get_data, find_numbers

inp = get_data(5)

memory = inp.split(",")
print(memory)


def param(memory, mode, ptr):
    val = int(memory[ptr])
    if mode == 0:
        # posmode
        return int(memory[val])
    elif mode == 1:
        # immediate mode
        return val


prog_input = 1


def run_prog(memory):
    prog_ptr = 0

    while True:
        to_exec = int(memory[prog_ptr])
        pmode1, pmode2, pmode3 = 0, 0, 0
        if to_exec > 4:
            # Parameter mode shit
            opcode = to_exec % 100

            pmode1 = int(to_exec / 100) % 10
            pmode2 = int(to_exec / 1000) % 10
            pmode3 = int(to_exec / 10000) % 10
        else:
            opcode = to_exec

        print(
            # f"Opcode {opcode}, pmodes ({pmode1} {pmode2} {pmode3}), raw {to_exec}",
        )

        if opcode == 1:
            # sum
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            assert pmode3 != 1
            res = int(memory[prog_ptr + 3])
            memory[res] = s1 + s2
            prog_ptr += 4

        elif opcode == 2:
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            assert pmode3 != 1
            res = int(memory[prog_ptr + 3])
            memory[res] = s1 * s2
            prog_ptr += 4

        elif opcode == 3:
            # input
            s1 = int(memory[prog_ptr + 1])
            memory[s1] = prog_input
            # print(f"Put input {prog_input} into loc {s1}")
            prog_ptr += 2
        elif opcode == 4:
            # output
            # print("outputting, memory is", memory)
            s1 = int(memory[prog_ptr + 1])
            # print("the ptr was", prog_ptr + 1, "and the val was", memory[s1])
            print(
                f"Intcode output instruction; memory={prog_ptr+1}, out is {memory[s1]}",
            )
            prog_ptr += 2
        elif opcode == 5:
            # jump if true
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            if s1 != 0:
                prog_ptr = s2
            else:
                prog_ptr += 3
        elif opcode == 6:
            # jump if false
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            if s1 == 0:
                prog_ptr = s2
            else:
                prog_ptr += 3
        elif opcode == 7:
            # less than
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            assert pmode3 != 1
            res = int(memory[prog_ptr + 3])
            if s1 < s2:
                memory[res] = 1
            else:
                memory[res] = 0
            prog_ptr += 4
        elif opcode == 8:
            # equals
            s1, s2 = (
                param(memory, pmode1, prog_ptr + 1),
                param(memory, pmode2, prog_ptr + 2),
            )
            assert pmode3 != 1
            res = int(memory[prog_ptr + 3])
            if s1 == s2:
                memory[res] = 1
            else:
                memory[res] = 0
            prog_ptr += 4
        elif to_exec == 99:
            # print("found 99, halting")
            break
        else:
            print("unexpected opcode " + str(to_exec))
            break

    return memory


# part 1
# print(run_prog(memory))
# print(run_prog([3, 0, 4, 0, 99]))

prog_input = 5
print(run_prog(memory))
