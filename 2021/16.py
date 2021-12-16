input = open("./16/input.txt", "r").readlines()

import bitstring

packet = input[0].strip()
# packet = "A0016C880162017C3686B18A3D4780"


c = bitstring.BitArray(hex=packet)

pos = 0

state = "head"
curtype = -1
curliteral = -1
curltypeid = -1
versionsum = 0


def parse(state, parse_bits, parse_packets, depth):
    global versionsum
    global pos
    curliteral = 0
    curoperator = -1
    literalparse = ""
    subpackets_length = -1
    num_subpackets = -1

    parsed_bits = 0
    parsed_packets = 0

    # import pdb

    # pdb.set_trace()

    while pos < len(c):
        print(" " * depth, "cur state", state, pos)
        if parse_bits:
            if parsed_bits == parse_bits:
                return
        if parse_packets:
            if parsed_packets == parse_packets:
                return

        if state == "head":
            v = c[pos : pos + 3].uint
            versionsum += v
            curtype = c[pos + 3 : pos + 6].uint
            pos += 6
            parsed_bits += 6
            if curtype == 4:
                state = "parse_lit"
            else:
                curoperator = curtype
                # operator
                ltype = c[pos : pos + 1].uint
                if ltype == 0:
                    subpackets_length = c[pos + 1 : pos + 16].uint
                    pos += 16
                    parsed_bits += 16
                    state = "parse_subp_len"
                elif ltype == 1:
                    num_subpackets = c[pos + 1 : pos + 12].uint
                    pos += 12
                    parsed_bits += 12
                    state = "parse_subp_num"

        elif state == "parse_lit":
            val = c[pos : pos + 5].uint
            if val & 0b10000 > 0:
                # there is more to read
                literalparse += c[pos + 1 : pos + 5]
                pos += 5
                parsed_bits += 5
            else:
                literalparse += c[pos + 1 : pos + 5]
                state = "head"
                parsed_packets += 1
                curliteral = literalparse.uint
                literalparse = ""
                pos += 5
                parsed_bits += 5
        elif state == "parse_subp_len":
            # for now just read the whole length
            # subps = c[pos:pos+subpackets_length]
            # todo parse them
            parse("head", subpackets_length, 0, depth + 1)
            parsed_packets += 1
            state = "head"

        elif state == "parse_subp_num":
            parse("head", 0, num_subpackets, depth + 1)
            parsed_packets += 1
            state = "head"


try:
    parse("head", 0, 0, 0)
except bitstring.InterpretError:
    pass
print(versionsum)

# state machine

# cur = 0
# state = "head"


# def read_n_bits(pos )


# for c in packet:
#     if c >= "0" and c <= "9":
#         cur = int(c)
#     elif c >= "A" and c <= "F":
#         cur = 10 + (ord(c) - ord("A"))

#     if state == "head":
#         v = cur & 0b111
#         state = "type"
#     elif state == "type":
#         tp = (cur & 0b111000) >> 3
