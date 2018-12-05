from get_data import get_data_lines, get_data

data = get_data(5).strip()


def remove_consecutive_runs(l):
    """
    >>> remove_consecutive_runs([2, 3, 4, 5, 7, 8, 10, 11, 12])
    [2, 3, 7, 8, 10, 11]

    >>> remove_consecutive_runs([2, 3, 5, 6, 7, 9, 10, 11, 12, 13])
    [2, 3, 5, 6, 9, 10]

    >>> remove_consecutive_runs([2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15])
    [2, 3, 5, 6, 9, 10, 15]

    >>> remove_consecutive_runs([0, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15])
    [0, 2, 3, 5, 6, 9, 10, 15]
    """
    # Remove consecutive runs of more than 2.
    l_copy = []
    num_consecutive = 0
    last_num = -10
    # print(l)
    for i in l:
        if i - last_num == 1:
            num_consecutive += 1
            # print('consecutive', i, last_num, num_consecutive)
        else:
            num_consecutive = 0
        if num_consecutive < 2:
            l_copy.append(i)
        last_num = i
    return l_copy


def reduce(data):
    while True:
        lc = None
        x = set()
        for i in range(len(data)):
            tc = data[i]
            if lc and tc.upper() == lc.upper() and tc != lc:
                x.add(i - 1)
                x.add(i)
            lc = tc

        if len(x) == 0:
            break

        new_data = ''
        to_remove = remove_consecutive_runs(list(set(x)))
        x = set(to_remove)

        for i in range(len(data)):
            if i not in x:
                new_data = new_data + data[i]

        data = new_data

    return data


if __name__ == '__main__':

    # reduced = reduce(data)
    # print(len(reduced))
    # reduced = reduce(reduced)
    # print(len(reduced))

    l1 = len(data)
    while True:
        for c in 'abcdefghijklmnopqrstuvwxyz':
            data = data.replace(c + c.upper(), '').replace(c.upper() + c, '')
        if len(data) == l1:
            break
        l1 = len(data)

    print(len(data))