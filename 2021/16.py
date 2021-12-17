input = open("./16/input.txt", "r").readlines()


packet = input[0].strip()

bstr = ""
for c in packet:
    bstr += format(int(c, 16), "04b")


versionsum = 0


def apply_operation(op, literals, depth):
    if op == 0:
        return sum(literals)
    elif op == 1:
        prod = 1
        for n in literals:
            prod *= n
        return prod
    elif op == 2:
        return min(literals)
    elif op == 3:
        return max(literals)
    elif op == 5:
        assert len(literals) == 2
        return +(literals[0] > literals[1])
    elif op == 6:
        assert len(literals) == 2
        return +(literals[0] < literals[1])
    elif op == 7:
        assert len(literals) == 2
        return +(literals[0] == literals[1])
    else:
        raise Exception(f"bad operation {op} -- {literals}")


def read(bstr, bits):
    r = bstr[:bits]
    return r, bstr[bits:]

def parse():
    global versionsum
    global bstr
    v, bstr = read(bstr, 3)
    versionsum += int(v, 2)
    tp, bstr = read(bstr, 3)
    tp = int(tp, 2)
    if tp == 4:
        reading = True
        sofar = ""
        while reading:
            nib, bstr = read(bstr, 5)
            reading = nib[0] == '1'
            sofar += nib[1:]
        return {'lit': int(sofar, 2)}

    ltyp, bstr = read(bstr, 1)
    if ltyp == '0':
        sublen, bstr = read(bstr, 15)
        sublen = int(sublen, 2)
        oldlen = len(bstr)
        arr = []
        while len(bstr) > oldlen - sublen:
            ret = parse()
            arr.append(ret)
        return {'arr': arr, 'op': tp}

    else:
        numsub, bstr = read(bstr, 11)
        numsub = int(numsub, 2)
        arr = []
        for i in range(numsub):
            ret = parse()
            arr.append(ret)
        return {'arr': arr, 'op': tp}


ret = parse()

print('p1: ', versionsum)
print(ret)


def process(obj):
    currentop = -1
    if 'op' in obj:
        currentop = obj['op']

    if 'arr' in obj:
        arr = []
        for m in obj['arr']:
            arr.append(process(m))
        if currentop != -1:
            return apply_operation(currentop, arr, 0)

    if 'lit' in obj:
        return obj['lit']


print('p2:', process(ret))

