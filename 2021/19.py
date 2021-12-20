input = open("./19/input.txt", "r").readlines()


scanners = []
potential_beacons = []


class Scanner:
    def __init__(self, n):
        self.n = n
        self.beacons = []
        self.beacon_diffs = []


cur_scanner = None

for l in input:
    l = l.strip()
    if "--- scanner" in l:
        cur_scanner = Scanner(int(l.split("--- scanner ")[1].split(" ")[0]))
        scanners.append(cur_scanner)

    elif l:
        x, y, z = l.split(",")
        beacon = (int(x), int(y), int(z))
        cur_scanner.beacons.append(beacon)
        potential_beacons.append(beacon)


print("nscanners:", len(scanners))
print("potentialbeacons", len(potential_beacons))

uniq_bcn_diffs = {}
overall_segments = {}


def build_beacon_diffs(s: Scanner):
    if s.beacon_diffs:
        return
    for i1 in range(len(s.beacons)):
        for i2 in range(i1 + 1, len(s.beacons)):
            s.beacon_diffs.append(
                (
                    f"s{s.n}-b{i1}",
                    f"s{s.n}-b{i2}",
                    (
                        s.beacons[i1][0] - s.beacons[i2][0],
                        s.beacons[i1][1] - s.beacons[i2][1],
                        s.beacons[i1][2] - s.beacons[i2][2],
                    ),
                )
            )


def to_invariant(tpl: tuple):
    return tuple(sorted([abs(x) for x in list(tpl)]))


def invariant_eq(tpl1: tuple, tpl2: tuple):
    return to_invariant(tpl1) == to_invariant(tpl2)


def find_bdiff_overlaps(s1: Scanner, s2: Scanner, i, j):
    return invariant_eq(s1.beacon_diffs[i][2], s2.beacon_diffs[j][2])


beacon_possibilities = {}
resolved_beacons = {}


def find_overlaps(s1: Scanner, s2: Scanner):
    # find overlaps between two scanners
    build_beacon_diffs(s1)
    build_beacon_diffs(s2)

    overlaps = set()
    global overall_segments

    for i in range(len(s1.beacon_diffs)):
        for j in range(len(s2.beacon_diffs)):
            overlapped = find_bdiff_overlaps(s1, s2, i, j)
            if overlapped:
                overlaps.add(s1.beacon_diffs[i][0])
                overlaps.add(s1.beacon_diffs[i][1])

                inv1 = to_invariant(s1.beacon_diffs[i][2])
                inv2 = to_invariant(s2.beacon_diffs[j][2])

                overall_segments[inv1] = overall_segments.get(inv1, []) + [
                    (s1.beacon_diffs[i][0], s1.beacon_diffs[i][1]),
                    (s2.beacon_diffs[j][0], s2.beacon_diffs[j][1]),
                ]

                overall_segments[inv2] = overall_segments.get(inv2, []) + [
                    (s1.beacon_diffs[i][0], s1.beacon_diffs[i][1]),
                    (s2.beacon_diffs[j][0], s2.beacon_diffs[j][1]),
                ]

    if len(overlaps) >= 12:
        print(len(overlaps), "overlaps between scanners", s1.n, s2.n, overlaps)


def add_possibility(i1, i2):
    global beacon_possibilities
    if i1 not in beacon_possibilities:
        beacon_possibilities[i1] = {}
    if i2 not in beacon_possibilities[i1]:
        beacon_possibilities[i1][i2] = 0
    beacon_possibilities[i1][i2] += 1


def reconcile():
    global beacon_possibilities
    global resolved_beacons
    # This is a hand-wavy number:
    confirmations = 2
    for k, v in overall_segments.items():
        # values look like
        # [('s0-b0', 's0-b1'), ('s1-b3', 's1-b8'), ('s0-b0', 's0-b1'), ('s1-b3', 's1-b8')]
        # [('s0-b0', 's0-b3'), ('s1-b3', 's1-b12'), ('s0-b0', 's0-b3'), ('s1-b3', 's1-b12')]
        # scanner0-beacon0 == s0-b0
        # so the line segment s0-b0 to s0-b1 corresponds to s1-b3 to s1-b8
        # and the line segment s0-b0 to s0-b3 corresponds to s1-b3 to s1-b12
        # which implies s0-b0 is s1-b3, s0-b1 is then s1-b8 and s0-b3 is s1-b12
        # etc.
        vset = set(v)
        for item1 in vset:
            for item2 in vset:
                if item1 == item2:
                    continue

                add_possibility(item1[0], item2[0])
                add_possibility(item1[1], item2[0])
                add_possibility(item1[0], item2[1])
                add_possibility(item1[1], item2[1])

    # now aggregate possibilities
    for k, v in beacon_possibilities.items():
        for k2, v2 in v.items():
            if v2 >= confirmations:
                if k not in resolved_beacons:
                    resolved_beacons[k] = set()
                resolved_beacons[k].add(k2)


for i1 in range(len(scanners)):
    print(f"finding overlaps... scanner {i1}")
    for i2 in range(i1 + 1, len(scanners)):
        overlaps = find_overlaps(scanners[i1], scanners[i2])

reconcile()

counted_beacons = set()

bcns = 0
for s in scanners:
    for idx, b in enumerate(s.beacons):
        bid = f"s{s.n}-b{idx}"
        if bid not in counted_beacons:
            counted_beacons.add(bid)
            bcns += 1
            if bid in resolved_beacons:
                for dup in resolved_beacons[bid]:
                    counted_beacons.add(dup)

print("p1:", bcns)
