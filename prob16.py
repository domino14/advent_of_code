import copy
import json
from collections import namedtuple, defaultdict
from get_data import get_data, get_data_lines


lines = get_data(16)
part_inputs = lines.split('\n\n\n')

observations = []
Observation = namedtuple('Observation', ['before', 'instruction', 'after'])
for observation in part_inputs[0].split('\n\n'):
    before, instruction, after = observation.split('\n')
    before = json.loads(before.split('Before: ')[1])
    after = json.loads(after.split('After: ')[1])
    instruction = [int(i) for i in instruction.split(' ')]
    observations.append(Observation(before, instruction, after))


program = part_inputs[1].split('\n')


opcodes = set([
    'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
    'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
])


def apply_opcode(opcode, instruction, registers):
    """ apply `opcode` to `registers`.
        instruction is a list
        [OPCODE (unknown), A, B, C]

        with two inputs (A, B) and an output (C)
    """
    a = int(instruction[1])
    b = int(instruction[2])
    output_reg = int(instruction[3])

    if opcode == 'addr':
        output = registers[a] + registers[b]
    elif opcode == 'addi':
        output = registers[a] + b
    elif opcode == 'mulr':
        output = registers[a] * registers[b]
    elif opcode == 'muli':
        output = registers[a] * b
    elif opcode == 'banr':
        output = registers[a] & registers[b]
    elif opcode == 'bani':
        output = registers[a] & b
    elif opcode == 'borr':
        output = registers[a] | registers[b]
    elif opcode == 'bori':
        output = registers[a] | b

    elif opcode == 'setr':
        output = registers[a]
    elif opcode == 'seti':
        output = a

    elif opcode == 'gtir':
        if a > registers[b]:
            output = 1
        else:
            output = 0
    elif opcode == 'gtri':
        if registers[a] > b:
            output = 1
        else:
            output = 0
    elif opcode == 'gtrr':
        if registers[a] > registers[b]:
            output = 1
        else:
            output = 0

    elif opcode == 'eqir':
        if a == registers[b]:
            output = 1
        else:
            output = 0
    elif opcode == 'eqri':
        if registers[a] == b:
            output = 1
        else:
            output = 0
    elif opcode == 'eqrr':
        if registers[a] == registers[b]:
            output = 1
        else:
            output = 0

    registers[output_reg] = output


def solve(observations, program):
    total_applying_opcodes = defaultdict(lambda: [])
    for obs in observations:
        applying_opcodes = []
        for opcode in opcodes:
            before = copy.deepcopy(obs.before)
            after = obs.after
            # obs[1][1:] is the last three numbers of the observation
            apply_opcode(opcode, obs.instruction, before)
            if all([before[x] == after[x] for x in range(4)]):
                # this opcode applies
                applying_opcodes.append(opcode)
        total_applying_opcodes[obs.instruction[0]].append(applying_opcodes)

    s = 0
    for ao, guesses in total_applying_opcodes.items():
        for subl in guesses:
            if len(subl) >= 3:
                s += 1
    print(f'Total observations: {len(observations)}')
    print(f'part 1: {s}')

    reduced = {}
    # Determine which opcode is which.
    for ao, guesses in total_applying_opcodes.items():
        last_set = None
        for subl in guesses:
            ss = set(subl)
            if last_set:
                last_set = ss & last_set
            else:
                last_set = ss
        reduced[ao] = last_set

    determined = {}
    while len(determined) < 16:
        for k, v in reduced.items():
            if len(v) == 1:
                determined[k] = list(v)[0]
                for k2, v2 in reduced.items():
                    if determined[k] in v2:
                        v2.remove(determined[k])

    # print(reduced)
    # print(determined)
    start = [0, 0, 0, 0]
    for program_line in program:
        if program_line == '':
            continue
        instruction = [int(i) for i in program_line.split(' ')]
        opcode = instruction[0]
        apply_opcode(determined[opcode], instruction, start)

    print(start)
    print(f'part 2: {start[0]}')


if __name__ == '__main__':
    solve(observations, program)
