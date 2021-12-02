input = open("/Users/cesar/01/input.txt", "r").read().strip()

lines = input.split("\n")
for l in lines:
    for m in lines:
        for r in lines:
            ln = int(l)
            lm = int(m)
            lr = int(r)
            if ln + lm + lr == 2020:
                print(ln * lm * lr)
                exit(1)


result = 0
print("Result: {}".format(result))