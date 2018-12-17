from get_data import get_data, get_data_lines


MAX_HP = 200
ATTK = 3

SORT_MULTIPLIER = 1000


def unit_reading_sort_key(unit):
    return unit.y * SORT_MULTIPLIER + unit.x


class Unit:
    ELF = 'E'
    GOBLIN = 'G'

    def __init__(self, id, tp, hp, atk, x, y):
        self.id = id
        self.tp = tp
        self.hp = hp
        self.atk = atk
        # x, y is 0,0 at top left, increase right and down
        self.x = x
        self.y = y
        self.alive = True

    def __str__(self):
        return f'<{self.tp}: @ ({self.x}, {self.y}) (HP = {self.hp})>'

    def __repr__(self):
        return self.__str__()

    def within_range(self, x, y):
        return (
            (self.y == y and (self.x == x + 1 or self.x == x - 1)) or
            (self.x == x and (self.y == y + 1 or self.y == y - 1))
        )

    def adjacent_to_enemy(self, units):
        adjacent = []
        for unit in units:
            if not unit.alive:
                continue
            if self.id == unit.id or self.tp == unit.tp:
                continue
            if self.within_range(unit.x, unit.y):
                adjacent.append(unit)
        # Sort by lowest HP, then reading order.
        return sorted(adjacent, key=lambda unit: (
                          unit.hp * SORT_MULTIPLIER * SORT_MULTIPLIER +
                          unit.y * SORT_MULTIPLIER + unit.x))

    def attack(self, unit):
        # print(f'{self.tp} ({self.x}, {self.y}) attacks {unit.tp} '
        #       f'({unit.x}, {unit.y})')
        unit.hp -= self.atk
        if unit.hp <= 0:
            unit.die()

    def die(self):
        print(f'Unit {self} has died :(')
        self.alive = False

    def find_targets_in_range(self, parsed_map, units):
        in_range = []
        for unit in units:
            if not unit.alive:
                continue
            if self.id == unit.id or self.tp == unit.tp:
                continue
            # consider the 4 pts in the cardinal directions from this unit.
            pts = check_in_range_pts(parsed_map, unit, units)
            in_range.extend(pts)
        return in_range

    def find_reachable(self, parsed_map, units, in_range):
        """
        this function finds the (x, y) points in in_range that are actually
        reachable from (self.x, self.y)
        """
        reachable = []
        for pt in in_range:
            r, cost, queue = self.is_reachable(parsed_map, units, pt)
            if r:
                reachable.append((pt, cost, queue))

        return reachable

    def other_unit_at(self, units, x, y):
        for unit in units:
            if not unit.alive:
                continue
            if unit.id != self.id and unit.x == x and unit.y == y:
                return True
        return False

    def is_reachable(self, parsed_map, units, pt):
        # attempt to walk to pt. some sort of bucket fill algorithm?
        queue = [(pt[0], pt[1], 0)]
        el_idx = -1

        while el_idx < len(queue) - 1:
            el_idx += 1
            x, y, ctr = queue[el_idx]
            # four closest cells
            ll = [(x + 1, y, ctr + 1),
                  (x - 1, y, ctr + 1),
                  (x, y + 1, ctr + 1),
                  (x, y - 1, ctr + 1)]
            ll_copy = []
            for cell in ll:
                x, y, cctr = cell[0], cell[1], cell[2]
                remove = False
                if parsed_map[y][x] == '#' or self.other_unit_at(units, x, y):
                    remove = True
                for inner_el in queue:
                    if (x == inner_el[0] and y == inner_el[1] and
                            inner_el[2] <= cctr):
                        remove = True
                        break

                if not remove:
                    ll_copy.append(cell)
            queue.extend(ll_copy)
            if x == self.x and y == self.y:
                break

        # print(f'In is reachable, pt={pt}, queue={queue}')
        for el in queue:
            if el[0] == self.x and el[1] == self.y:
                return True, el[2], queue  # cost

        return False, None, None

    def find_closest(self, reachable):
        reachable = sorted(
            reachable,
            key=lambda r: (r[1] * SORT_MULTIPLIER * SORT_MULTIPLIER +
                           r[0][1] * SORT_MULTIPLIER + r[0][0]))
        # sorted by cost, then Y, then X (reading order)
        # print(f'Closest sorted: {reachable}')
        return reachable[0]

    def move_to_closest(self, closest):
        # closest is a tuple. the second index is the queue.
        queue = closest[2]
        # find ourselves in the queue.
        our_cost = None
        for el in queue:
            if el[0] == self.x and el[1] == self.y:
                our_cost = el[2]
        # find the next item down costwise
        next_step = []
        for el in queue:
            if el[2] == our_cost - 1 and self.within_range(el[0], el[1]):
                next_step.append(el)

        next_step = sorted(
            next_step,
            key=lambda s: s[1] * 1000 + s[0])
        # print(f'Found next step: {next_step}')
        step = next_step[0]
        for s in next_step:
            assert abs(self.x - s[0]) + abs(self.y - s[1]) == 1

        self.x = step[0]
        self.y = step[1]


def check_in_range_pts(parsed_map, unit, units):
    in_range = []
    for pt in ((unit.x+1, unit.y), (unit.x-1, unit.y),
               (unit.x, unit.y+1), (unit.x, unit.y-1)):
        if parsed_map[pt[1]][pt[0]] == '.':
            # reachable but check that there are no units here either.
            units_exist = False
            for u in units:
                if u.alive and u.x == pt[0] and u.y == pt[1]:
                    units_exist = True
                    break
            if not units_exist:
                in_range.append(pt)

    return in_range


def print_map(parsed_map, units):
    sorted_units = sorted(units, key=unit_reading_sort_key)

    for y, m in enumerate(parsed_map):
        to_print = list(''.join(m))
        unit_health = []
        for unit in sorted_units:
            if unit.y == y and unit.alive:
                to_print[unit.x] = unit.tp
                unit_health.append(f'{unit.tp}({unit.hp})')
        print(''.join(to_print) + '\t' + ', '.join(unit_health))
    print()


def parse_map(battle_map, elf_attack_power):
    parsed_map = []
    units = []
    unit_id = 1
    for y, line in enumerate(battle_map):
        cur_line = []
        for x, chr in enumerate(line):
            if chr == '.' or chr == '#':
                cur_line.append(chr)
            elif chr == 'E' or chr == 'G':
                cur_line.append('.')
                unit = Unit(unit_id, chr, MAX_HP,
                            elf_attack_power if chr == 'E' else ATTK, x, y)
                units.append(unit)
                print(f'Added unit {unit}')
                unit_id += 1

        parsed_map.append(cur_line)
    return parsed_map, units


def new_round(parsed_map, units):
    srt = sorted(units, key=unit_reading_sort_key)
    # print(f'sorted units: {srt}')

    for unit in filter(lambda unit: unit.alive, srt):
        if (all_units_of_type_dead(units, Unit.ELF) or
                all_units_of_type_dead(units, Unit.GOBLIN)):
            return False  # round did not complete in its entirety.

        if not unit.alive:
            # The unit may have died mid-round.
            continue
        # 1) move AND attack!
        adjacent = unit.adjacent_to_enemy(units)
        if adjacent:
            # attack!
            # already sorted by HP and reading order.
            # print(f'Adjacent to {unit} are {adjacent}')
            unit.attack(adjacent[0])
        else:
            # move
            # find targets that are in range
            in_range = unit.find_targets_in_range(parsed_map, units)
            # print(f'In range of unit {unit}: ', in_range)
            reachable = unit.find_reachable(parsed_map, units, in_range)
            # print(f'Reachable from unit {unit}: ', reachable)
            if reachable:
                closest = unit.find_closest(reachable)
                # print(f'Chose a point: {closest}, moving to it')
                # finally, move to closest.
                if closest:
                    unit.move_to_closest(closest)
                    # we attack in the same turn!
                    adjacent = unit.adjacent_to_enemy(units)
                    if adjacent:
                        unit.attack(adjacent[0])
    return True


def all_units_of_type_dead(units, tp):
    return len(list(filter(lambda u: u.tp == tp and u.alive, units))) == 0


def setup_game(attack_power):
    # this works but is slow :(
    battle_map = list(filter(lambda y: y.strip() != '', """
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
    """.split('\n')))

    battle_map = get_data_lines(15)

    parsed_map, units = parse_map(battle_map, attack_power)
    print('Initially: ')
    print_map(parsed_map, units)
    round_counter = 0
    while True:
        print(f'************* NEW ROUND {round_counter + 1} **************')
        completed = new_round(parsed_map, units)
        print_map(parsed_map, units)
        if completed:
            round_counter += 1
            print(f'After {round_counter} rounds')
        else:
            print(f'Quitting after {round_counter} total rounds')
            break

    hp_sum = sum([u.hp for u in units if u.alive])
    print(f'Outcome: {round_counter * hp_sum}')
    return units


if __name__ == '__main__':
    attack_power = 3
    while True:
        attack_power += 1
        units = setup_game(attack_power)
        success = True
        for unit in units:
            if unit.tp == Unit.ELF and unit.alive is False:
                success = False
        if success:
            print(f'Did it with attack_power {attack_power}')
            break
