import datetime
from collections import defaultdict
from get_data import get_data


# data = get_data(4)
with open('./data4.txt') as f:
    data = f.read()

lines = data.split('\n')

sd = sorted(lines)


def parse_d(my_line):
    fields = my_line.split(' ')
    y, mth, d = fields[0][1:].split('-')
    h, m = fields[1][:-1].split(':')

    guard_number = fields[3]
    slept = False
    woke = False

    if guard_number.startswith('#'):
        guard_number = int(guard_number[1:])
    elif guard_number == 'asleep':
        slept = True
    elif guard_number == 'up':
        woke = True

    dt = datetime.datetime(int(y)+500, int(mth), int(d), int(h), int(m))

    return dt, guard_number, slept, woke


sleepy = defaultdict(dict)

awake = True
time_fell_asleep = None
last_gn = -1
start_time = None
for l in sd:
    dt, gn, slept, woke = parse_d(l)
    if gn != last_gn and gn not in ('asleep', 'up'):
        # We have a new guard.
        last_gn = gn
        start_time = dt
        awake = True
    else:
        if slept:
            awake = False
            time_fell_asleep = dt
        elif woke:
            awake = True

            # how long?
            if 'timeasleep' not in sleepy[last_gn]:
                sleepy[last_gn]['timeasleep'] = 0
                sleepy[last_gn]['mins'] = defaultdict(int)
            mins_asleep = (dt - time_fell_asleep).seconds / 60
            sleepy[last_gn]['timeasleep'] += mins_asleep

            for i in range(int(mins_asleep)):
                actual_dt = time_fell_asleep + datetime.timedelta(minutes=i)
                sleepy[last_gn]['mins'][actual_dt.minute] += 1

biggest = -1
biggest_g = 0

for guard, d in sleepy.items():
    if d['timeasleep'] > biggest:
        biggest = d['timeasleep']
        biggest_g = guard
        max_min_ct = -1
        max_min = -1
        for m, ct in d['mins'].items():
            if ct > max_min_ct:
                max_min_ct = ct
                max_min = m

print(biggest_g * max_min)

# -------

max_guard = None
max_min_ct = -1
max_min = -1
for guard, d in sleepy.items():
    for m, ct in d['mins'].items():
        if ct > max_min_ct:
            max_min_ct = ct
            max_min = m
            biggest_g = guard

print(biggest_g * max_min)
