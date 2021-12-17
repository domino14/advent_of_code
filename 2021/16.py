input = open("./16/input.txt", "r").readlines()


packet = input[0].strip()
# packet = "9C005AC2F8F0"

bstr = ""
for c in packet:
    bstr += format(int(c, 16), "04b")


# state = "head"
# curtype = -1
# curliteral = -1
# curltypeid = -1
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





# def parse(state, parse_bits, parse_packets, curoperator, depth):
#     global versionsum
#     global pos
#     curliteral = 0
#     curliterals = []
#     literalparse = ""
#     subpackets_length = -1
#     num_subpackets = -1

#     parsed_bits = 0
#     parsed_packets = 0
#     operator_applied = False
#     # import pdb
#     print("  " * depth, "entered with operator", curoperator)

#     # pdb.set_trace()
#     while pos < len(c):
#         print("  " * depth, "cur state", state, pos)
#         if parse_bits:
#             if parsed_bits == parse_bits:
#                 print("  " * depth, "parsed bits equal, apply operation", curoperator)
#                 return apply_operation(curoperator, curliterals, depth)
#         if parse_packets:
#             if parsed_packets == parse_packets:
#                 print("  " * depth, "parsed packets equal, apply operation", curoperator)
#                 return apply_operation(curoperator, curliterals, depth)

#         if state == "head":
#             try:
#                 v = c[pos : pos + 3].uint
#             except bitstring.InterpretError:
#                 break
#             versionsum += v
#             try:
#                 curtype = c[pos + 3 : pos + 6].uint
#             except bitstring.InterpretError:
#                 break
#             pos += 6
#             print("  " * depth, "v:", v, "type", curtype)

#             parsed_bits += 6
#             if curtype == 4:
#                 state = "parse_lit"
#             else:
#                 curoperator = curtype
#                 print("  " * depth, "set curoperator to ", curoperator)
#                 # operator
#                 try:
#                     ltype = c[pos : pos + 1].uint
#                 except bitstring.InterpretError:
#                     break
#                 if ltype == 0:
#                     try:
#                         subpackets_length = c[pos + 1 : pos + 16].uint
#                     except bitstring.InterpretError:
#                         break
#                     pos += 16
#                     parsed_bits += 16
#                     state = "parse_subp_len"
#                 elif ltype == 1:
#                     try:
#                         num_subpackets = c[pos + 1 : pos + 12].uint
#                     except bitstring.InterpretError:
#                         break
#                     pos += 12
#                     parsed_bits += 12
#                     state = "parse_subp_num"

#         elif state == "parse_lit":
#             val = c[pos : pos + 5].uint
#             if val & 0b10000 > 0:
#                 # there is more to read
#                 literalparse += c[pos + 1 : pos + 5]
#                 pos += 5
#                 parsed_bits += 5
#             else:
#                 literalparse += c[pos + 1 : pos + 5]
#                 state = "head"
#                 parsed_packets += 1
#                 curliteral = literalparse.uint
#                 curliterals.append(curliteral)
#                 print("  " * depth, "curliteral", curliteral, curliterals)
#                 literalparse = ""
#                 pos += 5
#                 parsed_bits += 5
#         elif state == "parse_subp_len":
#             # for now just read the whole length
#             # subps = c[pos:pos+subpackets_length]
#             # todo parse them
#             ret = parse("head", subpackets_length, 0, curoperator, depth + 1)
#             if type(ret) == list:
#                 curliterals.extend(ret)
#             else:
#                 curliterals.append(ret)
#             operator_applied = True
#             print("  " * depth, "ap", curliterals, "applied operator", curoperator)
#             parsed_packets += 1
#             state = "head"

#         elif state == "parse_subp_num":
#             ret = parse("head", 0, num_subpackets, curoperator, depth + 1)
#             if type(ret) == list:
#                 curliterals.extend(ret)
#             else:
#                 curliterals.append(ret)
#             operator_applied = True
#             print("  " * depth, "as", curliterals, "applied operator", curoperator)

#             parsed_packets += 1
#             state = "head"
#     if not operator_applied:
#         print("  "*depth, "operator", curoperator, "not applied yet, applying")
#         return apply_operation(curoperator, curliterals, depth)
#     else:
#         print("  "*depth, "operator",curoperator,"already applied")
#         return curliterals


# result = parse("head", 0, 0, -1, 0)

# print("p1: ", versionsum)
# print("p2: ", result)
