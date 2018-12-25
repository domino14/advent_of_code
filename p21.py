import copy

from get_data import get_data_lines
from prob16 import apply_opcode


registers = [0, 0, 0, 0, 0, 0]
program = get_data_lines(21)
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


print(f'solution: {registers[0]} (registers={registers}, cycles={cycles})')
