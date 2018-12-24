import copy
from prob16 import apply_opcode
from get_data import get_data_lines


program = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".split('\n')

# make this all 0s for the answer to part 1
registers = [0, 0, 0, 0, 0, 0]
program = get_data_lines(19)
parsed_program = []
current_ip = 0
for line in program:
    if line.startswith('#ip '):
        ip_register = int(line[4:])
        continue

    instruction = line.split(' ')
    parsed_program.append(instruction)


executing = True
cycles = 0
while executing:
    try:
        # print(f'Execute instruction, current_ip={current_ip}')
        registers[ip_register] = current_ip
        instruction = parsed_program[current_ip]
        # print(f' -> instruction={instruction}')
    except IndexError:
        break   # halt execution
    old_reg = copy.deepcopy(registers)
    apply_opcode(instruction[0], instruction, registers)
    print(f'executed: {current_ip}: {instruction} ({old_reg} -> {registers}')

    current_ip = registers[ip_register]
    current_ip += 1
    # print(f'Registers={registers}')
    cycles += 1
    # if cycles % 100000 == 0:
    #     print(f'Cycle {cycles}, registers={registers}')

print(f'solution: {registers[0]} (registers={registers}, cycles={cycles})')

# See decompilation notes for part 2 and prob19_decompiled.py
# This program is an extremely inefficient factorizer
# answer for part 1: sum(factors of p), p = 943
# answer for part 2: 1 + sum(factors of p), p = 10551343
# == 10553390
