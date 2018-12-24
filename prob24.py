from get_data import get_data_lines, find_numbers
from collections import defaultdict
desc = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".split('\n')

desc = [d for d in desc if d.strip() != '']
desc = get_data_lines(24)


class ArmyGroup:
    def __init__(self, loyalty, num_units, hp_per_unit, weakness, immunity,
                 attack,
                 attack_type, initiative, army_id):
        self.loyalty = loyalty
        self.num_units = num_units
        self.hp_per_unit = hp_per_unit
        self.weakness = weakness
        self.immunity = immunity
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.alive = True
        self.army_id = army_id

    def __repr__(self):
        return(f'<{self.loyalty} {self.army_id} '
               f'{self.num_units} @ {self.hp_per_unit} '
               f'(weak: {self.weakness} immune: {self.immunity}) '
               f'attack={self.attack} ({self.attack_type}) '
               f'initiative={self.initiative} '
               f'effective_power={self.effective_power()}>')

    def effective_power(self):
        return self.num_units * self.attack

    def fight(self, other):
        # print(f'{self} is attacking {other}')
        damage = self.effective_power()
        if self.attack_type in other.weakness:
            damage *= 2
        elif self.attack_type in other.immunity:
            damage = 0

        num_killed = min(int(damage / other.hp_per_unit), other.num_units)
        other.num_units -= num_killed
        if other.num_units == 0:
            other.alive = False


def assign_armies(immune_boost):
    armies = []
    army_id = 1
    for line in desc:
        if line.endswith(':'):
            loyalty = line.split(':')[0]
            army_id = 1
            continue
        numbers = find_numbers(line)
        nu = numbers[0]
        hp = numbers[1]
        attack = numbers[2] + (immune_boost if 'Immune' in loyalty else 0)
        initiative = numbers[3]
        weakness = []
        immunity = []

        if '(' in line:
            in_paren = line.split('(')[1].split(')')[0]
            dirs = in_paren.split('; ')
            for dir in dirs:
                if dir.startswith('immune to'):
                    dir = dir[len('immune to '):]
                    app = immunity
                elif dir.startswith('weak to'):
                    dir = dir[len('weak to '):]
                    app = weakness

                app.extend(dir.split(', '))

        attack_type = line.split(' damage ')[0].split(' ')[-1]
        full_id = f'{loyalty[:3]}{army_id}'
        armies.append(ArmyGroup(loyalty, nu, hp, weakness, immunity, attack,
                                attack_type, initiative, full_id))
        army_id += 1
    return armies


MLTP = 1000000000


def find_receiver(receiving_armies, attacker):

    damages_dealt = []
    for receiver in receiving_armies:
        atk_pwr = attacker.effective_power()
        if attacker.attack_type in receiver.weakness:
            atk_pwr *= 2
        elif attacker.attack_type in receiver.immunity:
            atk_pwr = 0
        if atk_pwr == 0:
            continue

        damages_dealt.append((atk_pwr, receiver))
    damages_dealt = sorted(damages_dealt, key=lambda d: -d[0])

    if not damages_dealt:
        return None
    damages_dealt = list(filter(lambda d: damages_dealt[0][0] == d[0],
                                damages_dealt))
    damages_dealt = sorted(damages_dealt,
                           key=lambda d: -(d[1].effective_power() * MLTP +
                                           d[1].initiative))
    return damages_dealt[0][1]


def assign_targets(armies):
    # print(f'Assigning targets...')
    armies = sorted(armies, key=lambda a: (
        -(a.effective_power() * MLTP + a.initiative)))
    # print(f'Sorted armies: {armies}')
    attackers = {}

    for attacker in armies:

        receiving_armies = list(filter(
            lambda a: (a.army_id not in attackers.values() and
                       a.alive and a.loyalty != attacker.loyalty), armies))

        receiving_army = find_receiver(receiving_armies, attacker)

        if not receiving_army:
            continue
        attackers[attacker.army_id] = receiving_army.army_id

    return attackers


def find_army(armies, army_id):
    for a in armies:
        if a.army_id == army_id:
            return a


def fight_done(armies):
    loyalties = defaultdict(int)
    for army in armies:
        if army.alive:
            loyalties[army.loyalty] += 1

    print(f'loyalties are now {loyalties}')

    if not loyalties:
        return True
    if len(loyalties) == 1:
        return True

    return False


def battle(armies):
    while True:
        # 1: target selection
        armies = list(filter(lambda a: a.alive, armies))

        attackers = assign_targets(armies)
        print(f'Targets: {attackers}')
        # selected target a, fight.
        attacker_keys = attackers.keys()
        attacker_keys = sorted(
            attacker_keys,
            key=lambda a: -find_army(armies, a).initiative)

        for attacker in attacker_keys:
            army = find_army(armies, attacker)
            defender = find_army(armies, attackers[attacker])
            army.fight(defender)

        if fight_done(armies):
            break
        # break
        print(f'Live armies: {list(filter(lambda a: a.alive, armies))}')


def determine_score(armies):
    lol = defaultdict(int)
    for army in armies:
        if army.alive:
            lol[army.loyalty] += 1

    assert len(lol) == 1

    winner = 'Infection' if lol['Infection'] > 0 else 'Immune System'
    num_units = 0

    for army in armies:
        if army.loyalty == winner:
            num_units += army.num_units

    print(f'winner={winner} units: {num_units}')
    return winner, num_units


if __name__ == '__main__':
    immune_boost = 49
    while True:
        # for part 0 just make immune_boost 0 and get rid of the loop.
        print(f'Trying boost {immune_boost}')
        armies = assign_armies(immune_boost)
        battle(armies)
        winner, num_units = determine_score(armies)
        if 'Immune' in winner:
            break
        immune_boost += 1
