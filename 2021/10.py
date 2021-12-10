input = open("/Users/cesar/10/input.txt", "r").readlines()


closers = {
    "(": ")",
    "{": "}",
    "<": ">",
    "[": "]",
}

inv_closers = {v: k for k, v in closers.items()}
incompletes = []


def find(line):
    open_chunks = []
    for c in list(line):
        if c in (closers.keys()):
            open_chunks.append(c)
        else:
            # closing character
            if c in closers.values() and open_chunks[-1] != inv_closers[c]:
                return c
            open_chunks = open_chunks[:-1]

    return None


total_score = 0
for l in input:
    ret = find(l.strip())
    score = {")": 3, "]": 57, "}": 1197, ">": 25137, None: 0}[ret]
    total_score += score
    if ret is None:
        incompletes.append(l.strip())

print(total_score)


# part two
def complete(line):
    # completes a line, that must be incomplete (as opposed to corrupted)
    open_chunks = []
    for c in list(line):
        if c in (closers.keys()):
            open_chunks.append(c)
        else:
            open_chunks = open_chunks[:-1]

    score = 0

    for l in reversed(open_chunks):
        score *= 5
        score += {"(": 1, "[": 2, "{": 3, "<": 4}[l]

    return score


scores = sorted([complete(l) for l in incompletes])
print(scores[len(scores) // 2])
